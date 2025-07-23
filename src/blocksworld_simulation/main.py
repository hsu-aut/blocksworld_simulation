from blocksworld_simulation.api.api import start_flask_thread
from blocksworld_simulation.simulation.simulation import start_pygame_mainloop

def main(): 
    # Start Flask in a separate thread
    start_flask_thread()
    
    # Run pygame on the main thread (required for macOS)
    start_pygame_mainloop()


if __name__ == "__main__":
    main()