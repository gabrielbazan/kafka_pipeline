import logging

from confluent_kafka import Consumer


class KafkaConsumer:
    def __init__(
        self,
        source_topic_name: str,
        consumer: Consumer,
        on_consumption=None,
    ) -> None:
        self.source_topic_name: str = source_topic_name
        self.consumer: Consumer = consumer
        self.on_consumption = on_consumption

    def consume(self):
        try:
            self.try_to_consume_topic()
        except KeyboardInterrupt:
            logging.warning("Stopping consumer as requested by user")
        except Exception:
            logging.exception("Failed to consume topic '%s'", self.source_topic_name)
        finally:
            self.consumer.close()

    def try_to_consume_topic(self):
        self.consumer.subscribe([self.source_topic_name])

        while True:
            message = self.consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                logging.error(
                    "An error occurred while reading message: %s", message.error()
                )
                continue

            self.handle_message(message)

    def handle_message(self, message):
        self.on_consumption(message)
