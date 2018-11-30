# TODOS

- ~~Rename the quote creator and retriever apis be something like dispatchers. They don't create/retrieve anything, the database wrapper does.~~
- Move database files into own database dir?
- Clean up the naming for prometheus stuff
- ~~Move configs to own directory~~
- ~~Put all gunicorn configs in gunigorn_config.py so the Dockerfile entrypoint can be gunicorn app:api~~
- Write tests:
  - test_api_utils.py
  - test_quote_creator.py
  - test_quote_retriever.py
  - test_metrics.py
- Use async requests when getting random quote from QUOTE_RESOURCE so getting n > 1 doesn't take n * request_time but rather takes (request_time1 + request_time2 + ...) / n average time
    - grequests
    - requests-threads
    - requests-futures
- Have a falcon hooks in the dispatchers for after that checks if an exception happened when trying to store/retrieve