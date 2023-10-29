import time
import threading

# Define a class for the expiring dictionary
class ExpiringDict:

    # Initialize the dictionary and the lock object
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    # Define a method to set a key and value pair with an expiration time
    def set(self, key, value, ttl=60):
        # Acquire the lock to avoid concurrent access
        with self.lock:
            # Store the current time and the time to live
            now = time.time()
            expire = now + ttl
            # Set the key and value pair in the dictionary
            self.dict[key] = (value, expire)
            # Start a timer thread to delete the item after the expiration time
            timer = threading.Timer(ttl, self.delete, args=[key])
            timer.start()

    # Define a method to get the value of a key from the dictionary
    def get(self, key):
        # Acquire the lock to avoid concurrent access
        with self.lock:
            # Check if the key exists in the dictionary
            if key in self.dict:
                # Get the value and the expiration time of the item
                value, expire = self.dict[key]
                # Check if the item is still valid
                if time.time() < expire:
                    # Return the value of the item
                    return value
                else:
                    # Delete the expired item from the dictionary
                    self.delete(key)
                    # Return None as the item is not found
                    return None
            else:
                # Return None as the key is not found
                return None

    # Define a method to delete a key from the dictionary
    def delete(self, key):
        # Acquire the lock to avoid concurrent access
        with self.lock:
            # Check if the key exists in the dictionary
            if key in self.dict:
                # Delete the key and value pair from the dictionary
                del self.dict[key]