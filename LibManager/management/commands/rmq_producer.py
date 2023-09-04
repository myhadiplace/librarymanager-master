from django.core.management.base import BaseCommand
from LibManager.Rmq_producer import main


class Command(BaseCommand):
    help = 'execute Rmq_producer'
    
    def handle(self,*args,**options):
        self.stdout.write(self.style.SUCCESS('Running RMQ producer script...'))
        main()
        self.stdout.write(self.style.SUCCESS('RMQ producer script executed successfully'))