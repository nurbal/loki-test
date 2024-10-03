import logging
import os
import opentelemetry

def main():
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource

    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
             "service.name": "testing",
             "service.instance.id": os.uname().nodename,
            }
         ),
    )
    set_logger_provider(logger_provider)

    endpoint = "http://loki01.server.mila.quebec:3100/otlp/v1/logs"

    otlp_exporter = OTLPLogExporter(endpoint) 
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)

    logger.info("Test info log")
    logger.debug("Test debug log")
    logger.warning("Test warning log")
    logger.error("Test error log")

    print ("os.uname().nodename: ", os.uname().nodename)



if __name__ == "__main__":
    main()