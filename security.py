FREE_GROUP_LIMIT = 3

def plan_allowed(plan, total_groups):
    if plan == "free" and total_groups > FREE_GROUP_LIMIT:
        return False
    return True