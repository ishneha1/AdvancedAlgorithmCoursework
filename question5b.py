"""
Multithreaded Sorting System - Functional Approach
Uses MergeSort with pure functions and helper utilities.
Emphasizes functional decomposition with separate thread management.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random
import time


# Pure functions for MergeSort algorithm
def merge_subarrays(left_arr, right_arr):
    """
    Merge two sorted arrays into one sorted array.
    Pure function: no side effects, returns new list.
    Time Complexity: O(n + m) where n and m are lengths of input arrays.
    """
    result = []
    i = j = 0
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            result.append(left_arr[i])
            i += 1
        else:
            result.append(right_arr[j])
            j += 1
    
    # Add remaining elements
    result.extend(left_arr[i:])
    result.extend(right_arr[j:])
    
    return result


def mergesort(arr):
    """
    Implement MergeSort using divide-and-conquer.
    Pure function: returns new sorted list without modifying input.
    Time Complexity: O(n log n) guaranteed.
    """
    if len(arr) <= 1:
        return arr[:]
    
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    
    return merge_subarrays(left, right)


def validate_integer_input(input_string):
    """
    Validate and parse user input into list of integers.
    Pure function: returns tuple (parsed_list, error_message).
    """
    try:
        if not input_string.strip():
            return None, "Cannot process empty input"
        
        # Handle both comma and space separated values
        cleaned = input_string.replace(',', ' ')
        parts = cleaned.split()
        
        if not parts:
            return None, "No values provided"
        
        integers = [int(p) for p in parts]
        
        if len(integers) < 2:
            return None, "Need at least 2 elements"
        
        return integers, None
    except ValueError as e:
        return None, f"Invalid number format: {str(e)}"


def split_array_halves(arr):
    """
    Split array into two equal halves.
    Pure function: returns tuple of (left_half, right_half).
    """
    mid = len(arr) // 2
    return arr[:mid], arr[mid:]


def create_status_message(thread_name, message, timestamp=True):
    """
    Create formatted status message for logging.
    Pure function: assembles message string.
    """
    if timestamp:
        return f"[{time.strftime('%H:%M:%S')}] {thread_name}: {message}"
    return f"{thread_name}: {message}"


class ThreadSafeDataStore:
    """Manages shared data and thread synchronization."""
    
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
        self.log_entries = []
    
    def set_data(self, key, value):
        """Thread-safe setter."""
        with self.lock:
            self.data[key] = value
    
    def get_data(self, key, default=None):
        """Thread-safe getter."""
        with self.lock:
            return self.data.get(key, default)
    
    def add_log(self, entry):
        """Add log entry thread-safely."""
        with self.lock:
            self.log_entries.append(entry)
    
    def get_logs(self):
        """Get all logs."""
        with self.lock:
            return self.log_entries[:]


class SortingCoordinator:
    """Coordinates the multithreaded sorting operation."""
    
    def __init__(self):
        self.store = ThreadSafeDataStore()
        self.threads = {}
    
    def sort_left_worker(self, left_arr):
        """Worker function for left sorting thread."""
        msg = create_status_message("THREAD_LEFT", "Starting to sort left half")
        self.store.add_log(msg)
        
        try:
            # Use MergeSort for efficient sorting
            sorted_left = mergesort(left_arr)
            self.store.set_data('left_sorted', sorted_left)
            
            msg = create_status_message("THREAD_LEFT", f"Completed. Sorted: {sorted_left}")
            self.store.add_log(msg)
        except Exception as e:
            msg = create_status_message("THREAD_LEFT", f"Error: {str(e)}")
            self.store.add_log(msg)
    
    def sort_right_worker(self, right_arr):
        """Worker function for right sorting thread."""
        msg = create_status_message("THREAD_RIGHT", "Starting to sort right half")
        self.store.add_log(msg)
        
        try:
            # Use MergeSort for efficient sorting
            sorted_right = mergesort(right_arr)
            self.store.set_data('right_sorted', sorted_right)
            
            msg = create_status_message("THREAD_RIGHT", f"Completed. Sorted: {sorted_right}")
            self.store.add_log(msg)
        except Exception as e:
            msg = create_status_message("THREAD_RIGHT", f"Error: {str(e)}")
            self.store.add_log(msg)
    
    def merge_worker(self, original_data):
        """Worker function for merging thread."""
        msg = create_status_message("THREAD_MERGE", "Waiting for sorting threads to complete")
        self.store.add_log(msg)
        
        try:
            # Wait for both sorting threads to finish using .join()
            self.threads['left'].join()
            self.threads['right'].join()
            
            msg = create_status_message("THREAD_MERGE", "Both sorting threads completed")
            self.store.add_log(msg)
            
            # Get sorted halves
            left_sorted = self.store.get_data('left_sorted', [])
            right_sorted = self.store.get_data('right_sorted', [])
            
            msg = create_status_message("THREAD_MERGE", f"Merging: {left_sorted} + {right_sorted}")
            self.store.add_log(msg)
            
            # Merge using pure function
            final_sorted = merge_subarrays(left_sorted, right_sorted)
            self.store.set_data('final_sorted', final_sorted)
            
            msg = create_status_message("THREAD_MERGE", f"Merge completed. Final: {final_sorted}")
            self.store.add_log(msg)
        except Exception as e:
            msg = create_status_message("THREAD_MERGE", f"Error: {str(e)}")
            self.store.add_log(msg)
    
    def execute_sorting(self, data):
        """Execute the complete sorting process."""
        # Clear previous data
        self.store.data = {}
        self.store.log_entries = []
        
        msg = create_status_message("SYSTEM", f"Received {len(data)} elements: {data}")
        self.store.add_log(msg)
        
        # Split data
        left_half, right_half = split_array_halves(data)
        msg = create_status_message("SYSTEM", f"Split into halves - Left: {left_half}, Right: {right_half}")
        self.store.add_log(msg)
        
        # Create threads
        self.threads['left'] = threading.Thread(target=self.sort_left_worker, args=(left_half,), daemon=False)
        self.threads['right'] = threading.Thread(target=self.sort_right_worker, args=(right_half,), daemon=False)
        self.threads['merge'] = threading.Thread(target=self.merge_worker, args=(data,), daemon=False)
        
        # Start threads
        self.threads['left'].start()
        self.threads['right'].start()
        self.threads['merge'].start()
    
    def wait_completion(self):
        """Wait for all threads to complete and return result."""
        if 'merge' in self.threads:
            self.threads['merge'].join()
        
        return self.store.get_data('final_sorted', [])


class ModernSortingGUI:
    """GUI for functional multithreaded sorting system."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multithreaded MergeSort System")
        self.root.geometry("1000x750")
        
        self.coordinator = SortingCoordinator()
        self.is_sorting = False
        
        self._build_interface()
    
    def _build_interface(self):
        """Build the GUI components."""
        # Container
        container = ttk.Frame(self.root, padding="12")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(container, text="Multithreaded MergeSort Coordinator",
                          font=("Arial", 16, "bold", "underline"))
        header.pack(pady=(0, 20))
        
        # Input section
        input_section = ttk.LabelFrame(container, text="Input Configuration", padding="12")
        input_section.pack(fill=tk.X, pady=8)
        
        ttk.Label(input_section, text="Enter numbers (comma or space separated):").pack(anchor=tk.W, pady=(0, 5))
        
        self.input_field = tk.Text(input_section, height=3, width=90)
        self.input_field.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        button_panel = ttk.Frame(input_section)
        button_panel.pack(fill=tk.X)
        
        ttk.Button(button_panel, text="▶ Execute Sort", command=self._execute_sort).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_panel, text="⚙ Generate Random (25)", command=self._generate_random).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_panel, text="✕ Clear All", command=self._clear_all).pack(side=tk.LEFT, padx=3)
        
        # Thread log section
        log_section = ttk.LabelFrame(container, text="Thread Execution Log", padding="12")
        log_section.pack(fill=tk.BOTH, expand=True, pady=8)
        
        # Log area with scrollbar
        scrollbar = ttk.Scrollbar(log_section)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_display = tk.Text(log_section, height=12, width=100, yscrollcommand=scrollbar.set)
        self.log_display.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_display.yview)
        
        # Results section
        results_section = ttk.LabelFrame(container, text="Results Display", padding="12")
        results_section.pack(fill=tk.X, pady=8)
        
        ttk.Label(results_section, text="Original Array:").pack(anchor=tk.W)
        self.original_display = tk.StringVar(value="[awaiting input]")
        ttk.Label(results_section, textvariable=self.original_display, font=("Courier", 11),
                 relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(3, 10))
        
        ttk.Label(results_section, text="Sorted Array:").pack(anchor=tk.W)
        self.sorted_display = tk.StringVar(value="[waiting for execution]")
        ttk.Label(results_section, textvariable=self.sorted_display, font=("Courier", 11),
                 relief=tk.SUNKEN, anchor=tk.W, foreground="darkgreen").pack(fill=tk.X, pady=3)
        
        # Status bar
        self.status_bar = tk.StringVar(value="Ready to start")
        status = ttk.Label(container, textvariable=self.status_bar, relief=tk.SUNKEN)
        status.pack(fill=tk.X, pady=(10, 0))
    
    def _execute_sort(self):
        """Execute sorting operation."""
        if self.is_sorting:
            messagebox.showwarning("Warning", "Sorting operation already in progress")
            return
        
        input_text = self.input_field.get()
        data, error = validate_integer_input(input_text)
        
        if error:
            messagebox.showerror("Validation Error", error)
            return
        
        self.is_sorting = True
        self.log_display.delete(1.0, tk.END)
        self.status_bar.set("Sorting operation in progress...")
        self.original_display.set(str(data))
        self.sorted_display.set("[Sorting...]")
        
        # Execute in separate thread to prevent GUI freeze
        exec_thread = threading.Thread(target=self._do_sorting, args=(data,), daemon=False)
        exec_thread.start()
    
    def _do_sorting(self, data):
        """Perform actual sorting and update UI."""
        try:
            # Start the sorting process
            self.coordinator.execute_sorting(data)
            
            # Wait for completion
            result = self.coordinator.wait_completion()
            
            # Update displays
            self.sorted_display.set(str(result))
            
            # Update log
            for log_entry in self.coordinator.store.get_logs():
                self.log_display.insert(tk.END, log_entry + "\n")
                self.log_display.see(tk.END)
            
            self.status_bar.set("✓ Sorting completed successfully")
            messagebox.showinfo("Success", "Multithreaded sorting completed!")
        except Exception as e:
            messagebox.showerror("Sorting Error", f"Operation failed: {str(e)}")
            self.status_bar.set("✗ Sorting failed")
        finally:
            self.is_sorting = False
    
    def _generate_random(self):
        """Generate random test data."""
        random_data = [random.randint(1, 100) for _ in range(25)]
        self.input_field.delete(1.0, tk.END)
        self.input_field.insert(1.0, " ".join(map(str, random_data)))
        self.status_bar.set(f"Generated {len(random_data)} random integers")
    
    def _clear_all(self):
        """Clear all displays."""
        self.input_field.delete(1.0, tk.END)
        self.log_display.delete(1.0, tk.END)
        self.original_display.set("")
        self.sorted_display.set("")
        self.status_bar.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSortingGUI(root)
    root.mainloop()
