from django.core.management.base import BaseCommand
from Trading.models import Stock, PriceData
from massive import RESTClient
from datetime import datetime


class Command(BaseCommand):
    help = "Pull historical stock data from Massive"

    def add_arguments(self, parser):
        parser.add_argument(
            "--ticker",
            type=str,
            default="AAPL",
            help="Stock ticker to download",
        )

        parser.add_argument(
            "--start",
            type=str,
            default="2026-01-01",
            help="Start date YYYY-MM-DD",
        )

        parser.add_argument(
            "--end",
            type=str,
            default="2026-10-08",
            help="End date YYYY-MM-DD",
        )

    def handle(self, *args, **options):

        ticker = options["ticker"].upper()
        start_date = options["start"]
        end_date = options["end"]

        self.stdout.write(
            f"Pulling {ticker} data from {start_date} to {end_date}..."
        )

        # Connect to Massive
        client = RESTClient()

        # Get or create stock
        stock, created = Stock.objects.get_or_create(
            ticker=ticker,
            defaults={
                "name": ticker,
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Stock: {ticker}")
            )

        count = 0

        try:
            # Request daily OHLCV data
            for bar in client.list_aggs(
                ticker,
                1,
                "day",
                start_date,
                end_date,
                adjusted="true",
                sort="asc",
                limit=50000,
            ):

                # Convert timestamp to date
                date = datetime.fromtimestamp(
                    bar.timestamp / 1000
                ).date()

                # Save to database
                PriceData.objects.update_or_create(
                    stock=stock,
                    date=date,
                    defaults={
                        "open_price": bar.open,
                        "high_price": bar.high,
                        "low_price": bar.low,
                        "close_price": bar.close,
                        "volume": bar.volume,
                        "adjusted_close": bar.close,
                    },
                )

                count += 1

                if count % 10 == 0:
                    self.stdout.write(
                        f"Downloaded {count} records..."
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully downloaded {count} records for {ticker}."
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error pulling data: {e}"
                )
            )