# calculate the agreement level
# needs NLTK package
# This function calculates the agreement between crowd workers in each round. 
# It uses Fleiss’ Kappa implementation in the NLTK package.
def calculate_round_kappa(round_estimates=[]):
    from nltk.metrics.agreement import AnnotationTask

    # Calculating the distance between two different estimate categories, and return the difference ratio
    def distance_cal(v1, v2):
        # all estimate categories: 1 hour, half a day, one day, half a week, one week, two weeks,
        # and more than two weeks (-1)
        labels = ['1.0', '4.0', '8.0', '20.0', '40.0', '80.0', '-1.0']
        i1 = labels.index(v1)
        i2 = labels.index(v2)
        return abs(i1 - i2) / 6

    # prepare estimate for the annotation task
    data, i = [], 1
    for estimate in round_estimates:
        data.append(["c" + str(i), 1, str(estimate)])
        i += 1

    task = AnnotationTask(data=data, distance=distance_cal)
    agreement_level = task.multi_kappa()
    return agreement_level


# The main goal of this function is to aggregate crowd estimate for each round and over 
# all the estimation session to come up with the final estimate.	
def aggregate_crowd_estimates(issues_estimates={}):
    import statistics
    issues_aggregated_estimates = {}
    for key,issue in issues_estimates.items():

        # get rounds count
        issue["round_count"] = len(issue["rounds"])

        # get Estimates info
        max_round_number=0
        estimates = issue["estimates"]
        issue["received_est"], issue["considered_est"], issue["discarded_est"] = len(issue["estimates"]),0,0

        for estimate in estimates:
            if estimate["quality_class"] in ("A","B"): # approved estimates are only A, and B classes
                if issue["considered_est"] < issue["round_count"] * 5:
                    issue["received_est"] += 1
                else:
                    issue["discarded_est"] += 1
            if estimate["quality_class"] in ("C", "D"):  # Rejected estimates are C, and D classes
                issue["discarded_est"] += 1

            if estimate["round_number"] > max_round_number:
                max_round_number = estimate["round_number"]

        # Aggregated Crowd Estimate
        last_round_estimates=[]
        for estimate in estimates:
            # only 5 estimates of the last round are considred and additional estimates are discarded even if they are
            # approved
            if estimate["round_number"] == max_round_number and len(last_round_estimates) < 6:
                last_round_estimates.append(estimate)

        issue_logged_time = estimates_hours_format(round(issue["logged_time"]/3600, 0))
        estimates = [int(e["value"]) for e in last_round_estimates]

        issue["crowd_estimate_median"] = remove_systamatic_bias(estimates_hours_format(statistics.median(estimates)),1)
        if issue["crowd_estimate_median"] < 1 : issue["crowd_estimate_median"] = 1 # 1 hour is the lowest categoty time

        issue["crowd_estimate_median_MRE"] = \
            int(round((abs(issue_logged_time - issue["crowd_estimate_median"])/issue_logged_time),0)*100)

        issue["crowd_estimate_median_category_time"] = estimates_time_category_format(issue["crowd_estimate_median"])

        issues_aggregated_estimates[key]=issue

    return issues_aggregated_estimates

# Two functions that are used to help in controlling the time format. 
# The first one: estimates_hours_format() to group estimates into estimate category. 
# There were seven categories as explained in the experiment publication. 
def estimates_hours_format (duration):
    duration = float(duration)
    if duration < 2:
        return 1
    elif duration < 6:
        return 4
    elif  duration < 11:
        return 8
    elif  duration < 31:
        return 20
    elif  duration < 61:
        return 40
    elif  duration < 121:
        return 80
    elif duration >= 121:
        return 121
    
# Tis function, estimates_time_category_format() do the same thing as estimates_hours_format() but it return the category name instead.
def estimates_time_category_format (duration):
    duration = float(duration)
    if duration < 2:
        return "One Hour"
    elif duration < 6:
        return "Half a day"
    elif  duration < 11:
        return "A day"
    elif  duration < 31:
        return "Half a week"
    elif  duration < 61:
        return "One week"
    elif  duration < 121:
        return "Two weeks"
    elif duration >= 121:
        return "More than two weeks"
