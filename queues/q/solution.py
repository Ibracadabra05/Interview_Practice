import queue  # If this import fails, you're probably using Python 2.
import json 
import hashlib
import hmac
import base64
import ast

class MsgService:
    """
        Ibra's implementation of a message service with a given set of
        transformation and dispatch rules. 
    """
    def __init__(self):
        self.msg_queue0 = queue.Queue()
        self.msg_queue1 = queue.Queue()
        self.msg_queue2 = queue.Queue()
        self.msg_queue3 = queue.Queue()
        self.msg_queue4 = queue.Queue()
        self.seq_dict = {}

    def transform(self,msg):
        for key, value in msg.items():
            if isinstance(value, (str)):
                if 'Qadium' in value:
                    msg[key] = self.rev(value)
            if isinstance(value, (int)):
                msg[key] = ~value
            if key is '_hash':
                v = msg[value]
                h = bytes(v).encode('utf-8')
                b = base64.b64encode(hmac.new(h, digestmod=hashlib.sha256).digest())
                msg['hash'] = b
    
    def enqueue(self, msg):
        #Handling messages that are not part of a sequence
        msg = ast.literal_eval(msg)
        if '_sequence' not in msg:
            self.transform(msg)
            queue_number = self.dispatch(msg)
        else:
            sequence = msg['_sequence']
            part = msg['_part']
            if (sequence in self.seq_dict) and (part in list(self.seq_dict.values())):
                print("No duplicate messages in sequence allowed. Please check part field of message.")
            elif sequence not in self.seq_dict:
                if part is not 0:
                    print("This is a new sequence and should thus begin with a message with part = 0")
                elif part is 0: 
                    self.transform(msg)
                    self.seq_dict[sequence][0] = self.dispatch(msg)
                    self.seq_dict[sequence][1] = 0
            else:
                if part == (self.seq_dict[sequence][1] + 1):
                    queue_to_dispatch = self.seq_dict[sequence][0]
                    #Keep track of previous message inserted in sequence
                    self.seq_dict[sequence][1] = part
                    self.transform(msg)
                    if queue_to_dispatch is 0:
                        self.msg_queue0.put(json.dumps(msg))
                    elif queue_to_dispatch is 1:
                        self.msg_queue1.put(json.dumps(msg))
                    elif queue_to_dispatch is 2:
                        self.msg_queue2.put(json.dumps(msg))
                    elif queue_to_dispatch is 3:
                        self.msg_queue3.put(json.dumps(msg))
                    elif queue_to_dispatch is 4:
                        self.msg_queue4.put(json.dumps(msg))
                else:
                    print("Messages in a sequence have to be passed into the service in ascending order. Please check part field of message.")

    def next(self, queue_number):
        try:
            if queue_number is 0:
                return self.msg_queue0.get(block=False)
            elif queue_number is 1:
                return self.msg_queue1.get(block=False)
            elif queue_number is 2:
                return self.msg_queue2.get(block=False)
            elif queue_number is 3:
                return self.msg_queue3.get(block=False)
            elif queue_number is 4:
                return self.msg_queue4.get(block=False)
        except queue.Empty:
            print("The queue you are trying to access is empty.")
            
    def search_for_key_of_val(self,msg, val):    
        for key, value in msg.items():
            if isinstance(value, (str)):
                if val in value:
                    return key
    
    def search_for_val_of_key(self,msg, key):    
        for the_key, the_value in msg.items():
            if the_key is key:
                return the_value
    
    def has_int_val(self,msg):
        for key, value in msg.items():
            if isinstance(value, (int)):
                return True
        return False
    
    def rev(self,s): 
        return s[::-1]
        
                    
    def dispatch(self,msg):
        queue_number = None
        if '_special' in msg:
            queue_number = 0
            self.msg_queue0.put(json.dumps(msg))
        elif 'hash' in msg:
            queue_number = 1
            self.msg_queue1.put(json.dumps(msg))
        elif self.search_for_key_of_val(msg,'muidaQ') is not None:
            queue_number = 2
            self.msg_queue2.put(json.dumps(msg))
        elif self.has_int_val(msg):
            queue_number = 3
            self.msg_queue3.put(json.dumps(msg))
        else:
            queue_number = 4
            self.msg_queue4.put(json.dumps(msg))
        return queue_number


def get_message_service():
    """Returns a new, "clean" Q service."""
    return MsgService()
