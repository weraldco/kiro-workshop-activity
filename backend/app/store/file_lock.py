"""
File locking mechanism for thread-safe file operations.

This module provides a FileLock context manager that ensures exclusive
access to files during write operations, preventing data corruption from
concurrent access.
"""

import fcntl
import os


class FileLock:
    """
    Context manager for exclusive file locking.
    
    Provides thread-safe file access by acquiring an exclusive lock
    on the file before operations and releasing it afterwards.
    
    Usage:
        with FileLock('/path/to/file.json'):
            # Perform file operations
            pass
    """
    
    def __init__(self, file_path: str):
        """
        Initialize file lock for given path.
        
        Args:
            file_path: Path to the file to lock
        """
        self.file_path = file_path
        self.lock_file = None
        self.lock_file_path = f"{file_path}.lock"
    
    def __enter__(self):
        """
        Acquire exclusive lock on file.
        
        Creates a lock file and acquires an exclusive lock using fcntl.
        Blocks until the lock is available.
        
        Returns:
            self
        """
        # Create lock file if it doesn't exist
        self.lock_file = open(self.lock_file_path, 'w')
        
        # Acquire exclusive lock (blocks until available)
        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Release lock on file.
        
        Releases the exclusive lock and closes the lock file.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        
        Returns:
            False to propagate any exceptions
        """
        if self.lock_file:
            # Release the lock
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
            
            # Close the lock file
            self.lock_file.close()
            
            # Clean up lock file
            try:
                os.remove(self.lock_file_path)
            except OSError:
                pass  # Lock file may have been removed already
        
        return False
