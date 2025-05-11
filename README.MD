# Random Pauper Commander

A discord bot that lets you play a game of rdph with your friends.

## Features

- Queue with custom amount of players
- Rerolls

### Prerequisites

- [Docker](https://www.docker.com/)

## Installation

```bash
git clone https://github.com/PXLCoarl/redh
cd redh
docker build -t rdph .
docker run -e TOKEN={your discord bot token} redh
