def run(payload):
    """orchestrates everything"""
    # ok ignore the payload stuff
    # idk how to get all this in here yet
    user = payload['user']
    course = payload['course']
    assignment = payload['assignment']
    commit = payload['commit']

    if not (user and course and assignment and commit):
        return 418, "missing one of: user. course, assignment, commit"
    if not user_in_course(course, user):
        return 403, "user not part of course on stogit"
    if not assignment_in_course(course, assignment):
        return 4XX, "unknown assignment"

    # TODO: how do we make sure to check all submitted assignments?
    # What if they complete several in one push?
    # How do they tell us that they re-submitted an assignment?

    # the preliminary checks are done!
    notify_user_begin(user, course, assignment)

    # go ahead and fetch the data now
    get_git_submission(user, commit)

    # check to see if all the files and folders are there
    check_expectations(course, assignment)
    check_mispellings(course, assignment)

    # I gave up on function arguments here. We'll need to think about how data is stored some more first

    # now for the fun part
    # static syntax-level checks for each file
    lint_submission()

    # recommended style checks for c++ code
    # i aint goving up on this one
    # ive seen too much hideous code come through for my liking
    # if it were up to me, this might even be a hard fail. something like:
    # > you can use whatever style you like in your own projects, but similarly to how papers are expected to be in Times, 11pt, code for this course is expected to follow these rules.
    analyze_submission_style()

    # compile each file as directed by the spec
    compile_submission()

    # perform any tests specified by the spec
    test_submission()

    # and we're done!
    # let the user know, give them any automated feedback, tell them how to re-submit the assignment, and that the code will still be checked by a grader.
    notify_user_completed()
