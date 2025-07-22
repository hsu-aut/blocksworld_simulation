from src.api.api import start_flask_thread
from src.simulation.simulation import start_pygame_mainloop

if __name__ == "__main__":
    # Start Flask in a separate thread
    start_flask_thread()
    
    # Run pygame on the main thread (required for macOS)
    start_pygame_mainloop()