import time
import numpy as np
import pandas as pd
import OpenDartReader
import FinanceDataReader as fdr

my_api = '' # 소연 api key
# my_api = '' # 내 api key

dart = OpenDartReader(my_api)

fs = dart.finstate