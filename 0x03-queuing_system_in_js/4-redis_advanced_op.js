import redis from 'redis';

const client = redis.createClient()

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error}`);
});

client.hset('HolbertonSchools', 'Portland', '50', print);
client.hset('HolbertonSchools', 'Seattle', '80', print);
client.hset('HolbertonSchools', 'New York', '20', print);
client.hset('HolbertonSchools', 'Bogota', '20', print);
client.hset('HolbertonSchools', 'Cali', '40', print);
client.hset('HolbertonSchools', 'Paris', '2', print);

client.hgetall('HolbertonSchools', (error, value) => {
  if (error) {
    console.log(error);
    throw error;
  }
  console.log(value);
});
