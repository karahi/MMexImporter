import sys
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
                             
def get_categoryid_for_payee(payee, categories, db):
  cat_id = -1
  sub_cat_id = -1
  for category in categories:
    if category in payee:
#       print "Match! '%s' - '%s'" %( category, payee)
      cat_str = categories[category][0]
    
      sub_cat_str = categories[category][1]
#       print "cat_str: %s, sub_cat_str: %s" %( cat_str, sub_cat_str)
      cat_id = db.get_categoryid(cat_str)
      if isinstance(sub_cat_str, ( int, long ) ):
        sub_cat_id = int(sub_cat_str)
      else:
        sub_cat_id = db.get_subcategoryid(sub_cat_str, cat_id)
      print "Payee: '%s' is being categorized as (%s:%s, %s:%s)" % (payee, cat_str, cat_id, sub_cat_str, sub_cat_id)
  return cat_id, sub_cat_id