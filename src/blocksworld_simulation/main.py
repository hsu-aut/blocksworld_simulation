import sys
import argparse
import logging
import threading 
from blocksworld_simulation.simulation.simulation import BlocksWorldSimulation
from blocksworld_simulation.api.api import api_to_sim_queue, sim_to_api_queue, run_flask


logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    # Parse args
    parser = argparse.ArgumentParser(description='Blocks World Simulation')
    parser.add_argument('--port', type=int, default=5001,
                       help='API server port (default: 5001)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='DEBUG', help='Logging level (default: DEBUG)')
    args = parser.parse_args()
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Start Flask in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    # Initialize simulation
    simulation = BlocksWorldSimulation(api_to_sim_queue, sim_to_api_queue)
    simulation.run()
    # if we reach here, it means the app should quit
    logger.info("Application quitting")
    sys.exit(0)
    
if __name__ == '__main__':
    main()