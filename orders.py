#------------------------------------------
# Import Libraies
#------------------------------------------

import pandas as pd
import numpy as np




# =============================================================================
# Prepaing and reading data
# =============================================================================

orders = pd.read_csv("data_orders.csv")
offers = pd.read_csv("data_offers.csv")
dataset = orders.merge(right=offers, how="inner", on="order_gk")


dataset["is_driver_assigned"] = np.where(dataset["is_driver_assigned_key"] == 1, "Yes", "No")
dataset["order_status"] = np.where(dataset["order_status_key"] == 4, "Client Cancelled", "System Reject")

dataset.drop(columns=["is_driver_assigned_key", "order_status_key"], inplace=True)

dataset = dataset.rename(columns={
    "order_datetime": "order_time"
})

# =============================================================================
# colors=['g','b','y','r']
# 
# cat_avg = dataset.groupby(["is_driver_assigned", "order_status"]).count()['order_gk']
# cat_list =  dataset['is_driver_assigned'] +","+ dataset['order_status']
# cat_list = cat_list.unique()
# 
# 
# 
# plt.title("Count by States")
# 
# for i in range(len(cat_list)):
#   print(cat_list[i])
#   plt.bar(cat_list[i],cat_avg[i],color=colors[i],label=cat_list[i])
# 
# plt.legend()
# plt.tight_layout()
# =============================================================================



# =============================================================================
# Question 1
# Build up a distribution of orders according to reasons for failure: 
#    cancellations before and after driver assignment, 
#    and reasons for order rejection. Analyse the resulting plot. 
#    Which category has the highest number of orders?
# =============================================================================

A1 = dataset.pivot_table(columns=["is_driver_assigned", "order_status"], values="order_gk", aggfunc="count")
A1.plot(kind="bar", subplots=False, figsize=(7, 7), legend=True, rot=0)



# =============================================================================
# Question 2
# Plot the distribution of failed orders by hours. 
# Is there a trend that certain hours have an abnormally high proportion of one category or another? 
# What hours are the biggest fails? How can this be explained?
# =============================================================================


dataset["hours"] = dataset["order_time"].str.split(":").apply(lambda split: split[0])

A2 = dataset.groupby(by=["hours", "is_driver_assigned", "order_status"])["order_gk"].count()
A2.reset_index().pivot(index="hours",columns=["is_driver_assigned", "order_status"],values="order_gk").plot(xticks=range(0, 24),figsize=(13, 7),title="Count of Failed Orders Per Hour and Category")




# =============================================================================
# Question 3
# Plot the average time to cancellation with and without driver, by hour. 
# Can we draw any conclusions from this plot?
# =============================================================================

A3 = dataset.groupby(by=["hours", "is_driver_assigned"])["cancellations_time_in_seconds"].mean()
A3.reset_index().pivot(index="hours",columns="is_driver_assigned",values="cancellations_time_in_seconds").plot(xticks=range(0, 24),figsize=(13, 7),title="Average Time to Cancellation Per Hour and Driver Assignment")





# =============================================================================
# Question 4
# Plot the distribution of average ETA by hours. How can this plot be explained?
# =============================================================================


Q4 = dataset.groupby(by="hours")["m_order_eta"].mean()
Q4.plot(figsize=(14, 7),xticks=range(0, 24),title="Average ETA per hour")































