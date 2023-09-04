from django.core.management.base import BaseCommand
from LibManager.Rmq_consumer import main


class Command(BaseCommand):
    help = 'execute Rmq_consumer'
    
    def handle(self,*args,**options):
        self.stdout.write(self.style.SUCCESS('Running RMQ consumer script...'))
        main()
        self.stdout.write(self.style.SUCCESS('RMQ consumer script executed successfully'))