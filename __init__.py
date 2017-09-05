# ------------------ #

def run_tests(*options):
    """
    Run all the automated tests on this module
    """
    import os, nose
    modulePath = os.path.split(__file__)[0]
    return nose.run(argv=['', modulePath] + list(options))
    
run_tests.__test__ = False

# ------------------ #

