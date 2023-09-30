const accountSid = process.env.ACCOUNT_SID;
const authToken = process.env.AUTH_TOKEN;
const client = require('twilio')(accountSid, authToken);
const Twilio_number = process.env.TWILIO_NUMBER


let callSid;
let recordingSid;

client.calls.list({ from: Twilio_number })
  .then(calls => {
    if (calls.length > 0) {
       callSid = calls[0].sid; // Assuming you want the latest call
      console.log('Call SID:', callSid);
      
      // Continue to fetch recording SID and download recording
    } else {
      console.log('No calls found.');
    }
  })
  .catch(error => {
    console.error('Error fetching calls:', error);
  });

 
//   // Assuming you have the callSid from step 1
client.recordings.list({ callSid: callSid })
.then(recordings => {
  if (recordings.length > 0) {
     recordingSid = recordings[0].sid; // Assuming you want the latest recording
    console.log('Recording SID:', recordingSid);

    // Continue to download recording
  } else {
    console.log('No recordings found for this call.');
  }
})
.catch(error => {
  console.error('Error fetching recordings:', error);
});

const fs = require('fs');

// Assuming you have the recordingSid from step 2
recordingSid = recordingSid; // Replace with the actual recording SID
const formatToFetch = 'json';

const recordingUrl = `https://api.twilio.com/2010-04-01/Accounts/${accountSid}/Recordings/${recordingSid}.${formatToFetch}`;

client.request({ method: 'GET', uri: recordingUrl })
  .then(response => {
    if (response.statusCode === 200) {
      const fileName = `${recordingSid}.${formatToFetch}`;
      const fileStream = fs.createWriteStream(fileName);
      response.pipe(fileStream);

      fileStream.on('finish', () => {
        console.log(`Recording downloaded to ${fileName}`);
      });
    } else {
    //   console.error('Error downloading recording:', response.statusMessage);
    console.error(`Error downloading recording (Status ${response.statusCode}): ${response.statusMessage}`);
    }
  })
  .catch(error => {
    console.error('Error downloading recording:', error);
  });
