import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const initialNumberOfSeats = 50;
let reservationEnabled = true;

const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
  const availableSeats = await getAsync('available_seats');
  return availableSeats ? parseInt(availableSeats, 10) : 0;
};

// Set the initial number of available seats
reserveSeat(initialNumberOfSeats);

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });
});

// Route to process the queue and decrease the number of available seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();
    const newAvailableSeats = currentAvailableSeats - 1;

    if (newAvailableSeats >= 0) {
      await reserveSeat(newAvailableSeats);
      done();
      console.log(`Seat reservation job ${job.id} completed`);
    } else {
      done(new Error('Not enough seats available'));
      console.log(`Seat reservation job ${job.id} failed: Not enough seats available`);
    }

    if (newAvailableSeats === 0) {
      reservationEnabled = false;
    }
  });
});

const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
