import os
import sys
import asyncio
import logging
from dska.swarm import SwarmManager
from dska.governance import GovernanceProtocol
from dska.scraper import SemanticsExtractor

# Initialize the DSKA system
def main():
    logging.basicConfig(level=logging.INFO)
    swarm_manager = SwarmManager()
    governance_protocol = GovernanceProtocol()
    semantics_extractor = SemanticsExtractor()

    # Start the DSKA system
    asyncio.run(swarm_manager.start())
    asyncio.run(governance_protocol.start())
    asyncio.run(semantics_extractor.start())

if __name__ == "__main__":
    main()