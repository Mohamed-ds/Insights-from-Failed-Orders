#------------------------------------------
# Import Libraies
#------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# =============================================================================
# Prepaing and reading data
# =============================================================================

orders = pd.read_csv("data_orders.csv")
offers = pd.read_csv("data_offers.csv")
dataset = orders.merge(right=offers, how="inner", on="order_gk")


dataset["is_driver_assigned"] = np.where(dataset["is_driver_assigned_key"] == 1, "Was_assigned", "Not_assigned")
dataset["order_status"] = np.where(dataset["order_status_key"] == 4, "Client Cancelled", "System Reject")

dataset.drop(columns=["is_driver_assigned_key", "order_status_key"], inplace=True)

dataset = dataset.rename(columns={
    "order_datetime": "order_time"
})


# =============================================================================
# Question 1
# Build up a distribution of orders according to reasons for failure: 
#    cancellations before and after driver assignment, 
#    and reasons for order rejection. Analyse the resulting plot. 
#    Which category has the highest number of orders?
# My opinion:
# There are 13435 orders canceled by the client, and 9469 rejected by the system.
# The high number of orders canceled before a driver is assigned implies that maybe customers have waited too long and have decided to choose an alternative for their transportation needs. 
# There are 8360 client cancellations after a driver has been assigned, and only four were rejected by the system.

# =============================================================================

A1 = dataset.pivot_table(columns=["is_driver_assigned", "order_status"], values="order_gk", aggfunc="count")

p1 = A1.plot(kind="bar", subplots=False, figsize=(7, 7), legend=True, rot=0)


# =============================================================================
# Question 2
# Plot the distribution of failed orders by hours. 
# Is there a trend that certain hours have an abnormally high proportion of one category or another? 
# What hours are the biggest fails? How can this be explained?

# My opinion:
# For the four offers rejected by the system, those were at 12 midnight. 
# The rest of the categories follow a similar distribution.
# the biggest fail hours are at 8 AM.

# =============================================================================

plt.figure()
dataset["hours"] = dataset["order_time"].str.split(":").apply(lambda split: split[0])

p2 = dataset.groupby(by="hours")["order_gk"].count().plot(figsize=(10, 7),
                                                         legend=True,
                                                         xticks=range(0, 24),
                                                         title="Count of Failed Orders by Hour of Day")

A2 = dataset.groupby(by=["hours", "is_driver_assigned", "order_status"])["order_gk"].count()
plt.figure()
p2 = A2.reset_index().pivot(index="hours",
                                   columns=["is_driver_assigned", "order_status"],
                                   values="order_gk").plot(xticks=range(0, 24),
                                                           figsize=(13, 7),
                                                           title="Count of Failed Orders Per Hour and Category")
                                                           
                                                           
                                                           

                                                          
                                                           
                                                           
# =============================================================================
# Question 3
# Plot the average time to cancellation with and without driver, by hour. 
# Can we draw any conclusions from this plot?

# My opinion:
# The average time to cancellation is always higher on orders with an assigned driver than without. 
# At 3 A.M. the average time to cancellation arrive at the top, At this time there are a lot of client cancellations.

# =============================================================================


plt.figure() 
A3 = dataset.groupby(by=["hours", "is_driver_assigned"])["cancellations_time_in_seconds"].mean()
p3 = A3.reset_index().pivot(index="hours",columns="is_driver_assigned",values="cancellations_time_in_seconds").plot(xticks=range(0, 24),figsize=(13, 7),title="Average Time to Cancellation Per Hour and Driver Assignment")


# =============================================================================
# Question 4
# Plot the distribution of average ETA by hours. How can this plot be explained?


# My opinion:
# The number of failed orders increases as the average waiting time of the client increases.

# =============================================================================

plt.figure()
A4 = dataset.groupby(by="hours")["m_order_eta"].mean()
p4 = A4.plot(figsize=(14, 7),xticks=range(0, 24),title="Average ETA per hour")




