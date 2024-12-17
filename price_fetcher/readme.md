Description:
This is the Readme file for Close Price Fetcher script.


Goal:
- To fetch the close price for BTC-USD for the month of June.

Assumptions:
1. Low Frequency Run: This is low frequency script( run few time only).
2. Availability: Service is mostly available anytime in day.
3. Time Consistency: Api given date range is acceptable by external client limit.
4. Return Data Constraint: The return data is not pagination and payload received is within acceptable range, not causing data transfer issue.
5. No Data Response: if no data is found it will return empty dict.
6. API Responses: Expected response 200 for success, other as fail.
7. Latency Concern: Latency of the external api is within https response timeout.
8. Network Errors: on this retry after some time should resolve it.

Implementation:
- main.py script is created which will invoke the code that will fetch the close data from the given instrument.
- The code is written to support other inputs and if flexible to extend for future use case with minimal code change.
- We have utilized code design pattern like Builder, factory to make the code more robust to change.
- The code is design to support multiple broker, instruments and different price values from OHLC.

Project Structure and Explanation:
Directories:
src -> interactor : this module consist the code that run broker specific code for multiple use case, the broker class 
is generated on runtime dynamically.
       configs : since, each broker or strategy can have different config is needed sometime, so to allow sceanario.
specific config this is design is used.
       errors : this consist of custom exception that are required.
       models : Consist of response and request pydantic schema for the payload.
test -> configs : unit test case for configs
        errors : unit test case for errors (custom exceptions)
        interactor : unit test case for interactor module for multiple broker support


How to Run:

Setup:
_(setup virtual env, if not already present)_

1. open file poetry_install run that script or run below commands: 
 `pip3 install poetry
  poetry install
  pip3 install pytest` # for dev env

2. run main.py script (update the parameters for config file for differ use case)
   `python main.py`

3. expected output:
   dict(timestamp="closePrice")

Testing:
for unit test execute from the parent directory:
`pytest -v -s --maxfail=1 test/`