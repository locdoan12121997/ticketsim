#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:50:23 2020

@author: kevin
"""

import json
import random
from collections import defaultdict

import numpy as np
import simpy
from kafka import KafkaProducer

# -------------------------
#  CONFIGURATION
# -------------------------

BUS_ARRIVAL_MEAN = 3
BUS_OCCUPANCY_MEAN = 100
BUS_OCCUPANCY_STD = 30

PURCHASE_RATIO_MEAN = 0.4
PURCHASE_GROUP_SIZE_MEAN = 2.25
PURCHASE_GROUP_SIZE_STD = 0.50

TIME_TO_WALK_TO_SELLERS_MEAN = 1
TIME_TO_WALK_TO_SELLERS_STD = 0.1
TIME_TO_WALK_TO_SCANNERS_MEAN = 0.5
TIME_TO_WALK_TO_SCANNERS_STD = 0.05

SELLER_LINES = 6
SELLERS_PER_LINE = 1
SELLER_MEAN = 1
SELLER_STD = 0.2

SCANNER_LINES = 4
SCANNERS_PER_LINE = 1
SCANNER_MEAN = 1 / 20
SCANNER_STD = 0.01

# Let's pre-generate all the bus arrival times and their occupancies so that even if we
# change the configuration, we'll have consistent arrivals
random.seed(42)
# ARRIVALS = [random.expovariate(1 / BUS_ARRIVAL_MEAN) for _ in range(400000)]
# ON_BOARD = [int(random.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD)) for _ in range(400000)]

# -------------------------
#  ANALYTICAL GLOBALS
# -------------------------

arrivals = defaultdict(lambda: 0)
seller_waits = defaultdict(lambda: [])
scan_waits = defaultdict(lambda: [])
event_log = []
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))


def register_arrivals(time, num):
    arrivals[int(time)] += num


def register_seller_wait(time, wait):
    seller_waits[int(time)].append(wait)


def register_scan_wait(time, wait):
    scan_waits[int(time)].append(wait)


def avg_wait(raw_waits):
    waits = [w for i in raw_waits.values() for w in i]
    return round(np.mean(waits), 1) if len(waits) > 0 else 0


def register_bus_arrival(time, bus_id, people_created):
    register_arrivals(time, len(people_created))
    # print(f"Bus #{bus_id} arrived at {time} with {len(people_created)} people")
    event = {
        "time": round(time, 2),
        "busId": bus_id,
        "firstId": people_created[0],
        "lastId": people_created[-1]
    }
    event_log.append({
        "event": "BUS_ARRIVAL",
        "time": round(time, 2),
        "busId": bus_id,
        "peopleCreated": people_created
    })
    producer.send('bus_arrival', event)


def register_group_moving_from_bus_to_seller(people, walk_begin, walk_end, seller_line, queue_begin, queue_end,
                                             sale_begin, sale_end):
    wait = queue_end - queue_begin
    service_time = sale_end - sale_begin
    register_seller_wait(queue_end, wait)
    # print(f"Purchasing group of {len(people)} waited {wait} minutes in Line {seller_line},"
    #       f" needed {service_time} minutes to complete")
    walk_to_seller_event = {
        "people": people,
        "sellerLine": seller_line,
        "time": round(walk_begin, 2),
        "duration": round(walk_end - walk_begin, 2)
    }
    event_log.append({
        "event": "WALK_TO_SELLER",
        "people": people,
        "sellerLine": seller_line,
        "time": round(walk_begin, 2),
        "duration": round(walk_end - walk_begin, 2)
    })
    producer.send('walk_to_seller', walk_to_seller_event)
    wait_in_seller_line_event = {
        "sellerLine": seller_line,
        "time": round(queue_begin, 2),
        "duration": round(queue_end - queue_begin, 2),
        "firstId": people[0],
        "lastId": people[-1]
    }
    event_log.append({
        "event": "WAIT_IN_SELLER_LINE",
        "people": people,
        "sellerLine": seller_line,
        "time": round(queue_begin, 2),
        "duration": round(queue_end - queue_begin, 2)
    })
    producer.send('wait_in_seller_line', wait_in_seller_line_event)
    buy_tickets_event = {
        "people": people,
        "sellerLine": seller_line,
        "time": round(sale_begin, 2),
        "duration": round(sale_end - sale_begin, 2)
    }
    event_log.append({
        "event": "BUY_TICKETS",
        "people": people,
        "sellerLine": seller_line,
        "time": round(sale_begin, 2),
        "duration": round(sale_end - sale_begin, 2)
    })
    producer.send('buy_tickets', buy_tickets_event)


def register_visitor_moving_to_scanner(person, walk_begin, walk_end, scanner_line, queue_begin, queue_end, scan_begin,
                                       scan_end):
    wait = queue_end - queue_begin
    service_time = scan_end - scan_begin
    register_scan_wait(queue_end, wait)
    # print(f"Scanning customer waited {wait} minutes in Line {scanner_line}, needed {service_time} minutes to complete")
    walk_to_scanner_event = {
        "person": person,
        "scannerLine": scanner_line,
        "time": round(walk_begin, 2),
        "duration": round(walk_end - walk_begin, 2)
    }
    event_log.append({
        "event": "WALK_TO_SCANNER",
        "person": person,
        "scannerLine": scanner_line,
        "time": round(walk_begin, 2),
        "duration": round(walk_end - walk_begin, 2)
    })
    producer.send('walk_to_scanner', walk_to_scanner_event)

    wait_in_scanner_line_event = {
        "person": person,
        "scannerLine": scanner_line,
        "time": round(queue_begin, 2),
        "duration": round(queue_end - queue_begin, 2)
    }
    event_log.append({
        "event": "WAIT_IN_SCANNER_LINE",
        "person": person,
        "scannerLine": scanner_line,
        "time": round(queue_begin, 2),
        "duration": round(queue_end - queue_begin, 2)
    })
    producer.send('wait_in_scanner_line', wait_in_scanner_line_event)

    scan_tickets_event = {
        "person": person,
        "scannerLine": scanner_line,
        "time": round(scan_begin, 2),
        "duration": round(scan_end - scan_begin, 2)
    }
    event_log.append({
        "event": "SCAN_TICKETS",
        "person": person,
        "scannerLine": scanner_line,
        "time": round(scan_begin, 2),
        "duration": round(scan_end - scan_begin, 2)
    })
    producer.send('scan_tickets', scan_tickets_event)


def pick_shortest(lines):
    """
        Given a list of SimPy resources, determine the one with the shortest queue.
        Returns a tuple where the 0th element is the shortest line (a SimPy resource),
        and the 1st element is the line # (1-indexed)

        Note that the line order is shuffled so that the first queue is not disproportionally selected
    """
    shuffled = list(zip(range(len(lines)), lines))  # tuples of (i, line)
    random.shuffle(shuffled)
    shortest = shuffled[0][0]
    for i, line in shuffled:
        if len(line.queue) < len(lines[shortest].queue):
            shortest = i
            break
    return lines[shortest], shortest + 1


def bus_arrival(env, seller_lines, scanner_lines):
    """
        Simulate a bus arriving every BUS_ARRIVAL_MEAN minutes with
        BUS_OCCUPANCY_MEAN people on board

        This is the top-level SimPy event for the simulation: all other events
        originate from a bus arriving
    """
    # Note that these unique IDs for busses and people are not required, but are included for eventual visualizations
    next_bus_id = 0
    next_person_id = 0
    while True:
        next_bus = random.expovariate(1 / BUS_ARRIVAL_MEAN)
        on_board = int(random.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD))
        # next_bus = ARRIVALS.pop()
        # on_board = ON_BOARD.pop()

        # Wait for the bus
        # bus_log.next_bus(next_bus)
        yield env.timeout(next_bus)
        # bus_log.bus_arrived(on_board)

        # register_bus_arrival() below is for reporting purposes only
        people_ids = list(range(next_person_id, next_person_id + on_board))
        register_bus_arrival(env.now, next_bus_id, people_ids)
        next_person_id += on_board
        next_bus_id += 1

        while len(people_ids) > 0:
            remaining = len(people_ids)
            group_size = min(round(random.gauss(PURCHASE_GROUP_SIZE_MEAN, PURCHASE_GROUP_SIZE_STD)), remaining)
            people_processed = people_ids[-group_size:]  # Grab the last `group_size` elements
            people_ids = people_ids[:-group_size]  # Reset people_ids to only those remaining

            # Randomly determine if this group is going to the sellers or straight to the scanners
            if random.random() > PURCHASE_RATIO_MEAN:
                env.process(scanning_customer(env, people_processed, scanner_lines,
                                              TIME_TO_WALK_TO_SELLERS_MEAN + TIME_TO_WALK_TO_SCANNERS_MEAN,
                                              TIME_TO_WALK_TO_SELLERS_STD + TIME_TO_WALK_TO_SCANNERS_STD))
            else:
                env.process(purchasing_customer(env, people_processed, seller_lines, scanner_lines))


def purchasing_customer(env, people_processed, seller_lines, scanner_lines):
    walk_begin = env.now
    yield env.timeout(random.gauss(TIME_TO_WALK_TO_SELLERS_MEAN, TIME_TO_WALK_TO_SELLERS_STD))
    walk_end = env.now

    queue_begin = env.now
    seller_line = pick_shortest(seller_lines)
    with seller_line[0].request() as req:
        # Wait in line
        # sellers.add_to_line(seller_line[1])
        yield req
        # sellers.remove_from_line(seller_line[1])
        queue_end = env.now

        # Buy tickets
        sale_begin = env.now
        yield env.timeout(random.gauss(SELLER_MEAN, SELLER_STD))
        sale_end = env.now

        register_group_moving_from_bus_to_seller(people_processed, walk_begin, walk_end, seller_line[1], queue_begin,
                                                 queue_end, sale_begin, sale_end)

        env.process(scanning_customer(env, people_processed, scanner_lines, TIME_TO_WALK_TO_SCANNERS_MEAN,
                                      TIME_TO_WALK_TO_SCANNERS_STD))


def scanning_customer(env, people_processed, scanner_lines, walk_duration, walk_std):
    # Walk to the seller
    walk_begin = env.now
    scan_time = random.gauss(walk_duration, walk_std)
    yield env.timeout(scan_time)
    walk_end = env.now

    # We assume that the visitor will always pick the shortest line
    queue_begin = env.now
    scanner_line = pick_shortest(scanner_lines)
    with scanner_line[0].request() as req:
        # Wait in line
        for _ in people_processed:
            # scanners.add_to_line(scanner_line[1])
            pass
        yield req
        for _ in people_processed:
            # scanners.remove_from_line(scanner_line[1])
            pass
        queue_end = env.now

        # Scan each person's tickets
        for person in people_processed:
            scan_begin = env.now
            yield env.timeout(random.gauss(SCANNER_MEAN, SCANNER_STD))  # Scan their ticket
            scan_end = env.now
            register_visitor_moving_to_scanner(person, walk_begin, walk_end, scanner_line[1], queue_begin, queue_end,
                                               scan_begin, scan_end)


# env = simpy.rt.RealtimeEnvironment(factor = 0.01, strict = False)
env = simpy.Environment()

seller_lines = [simpy.Resource(env, capacity=SELLERS_PER_LINE) for _ in range(SELLER_LINES)]
scanner_lines = [simpy.Resource(env, capacity=SCANNERS_PER_LINE) for _ in range(SCANNER_LINES)]

env.process(bus_arrival(env, seller_lines, scanner_lines))
# env.process(create_clock(env))
env.run(until=15000)

# main.mainloop()

with open('output/events.json', 'w') as outfile:
    json.dump({
        "sellerLines": SELLER_LINES,
        "scannerLines": SCANNER_LINES,
        "events": event_log
    }, outfile)
