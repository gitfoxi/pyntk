
def run():
  import unittest
  import sys

  sys.path.append('../scripts')
  try:
    test_keyclient
    reload(test_keyclient)
  except:
    import test_keyclient
  #suite = unittest.defaultTestLoader.discover('../scripts')
  #unittest.TextTestRunner(verbosity=2).run(suite)

  unittest.main( exit=False, verbosity=2, module=test_keyclient )


