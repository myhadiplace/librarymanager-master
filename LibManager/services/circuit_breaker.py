import time

class CircuitBreaker:
    def __init__(self,filure_threshold,reset_timeout):
        self.filure_threshold = filure_threshold
        self.reset_timeout = reset_timeout
        self.failure = 0
        self.state = 'close'
        self.last_failure_time = None

    def execution(self,operation):
        if self.state == 'open':
            if time.time() - self.last_failure_time >= self.reset_timeout:
                self.reset_circuit()
                return True
        elif self.state == 'close':
            try:
                result = operation()
                self.reset_circuit()
            except Exception as e:
                self.handle_failure()

        
    def reset_circuit(self):
        self.failure = 0
        self.state = 'close'
        self.last_failure_time = None
    
    def handle_failure(self):
        self.failure += 1
        print('circuite failure')
        if self.failure >= self.filure_threshold:
            self.state == 'open'
            return False


    
