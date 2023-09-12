exports.handler = function (context, event, callback) {
    // The pre-initialized Twilio Client is available from the `context` object
    const twilioClient = context.getTwilioClient();
  
    // Query parameters or values sent in a POST body can be accessed from `event`
    const from = event.From || '+12024558976';
    const to = event.To || '+918448935901';
    // Note that TwiML can be hosted at a URL and accessed by Twilio
    const url = event.Url || 'https://voicebotdemo-9971-dev.twil.io/transcribe';

    const record = event.Record || true;
  
    // Use `calls.create` to place a phone call. Be sure to chain with `then`
    // and `catch` to properly handle the promise and call `callback` _after_ the
    // call is placed successfully!
    twilioClient.calls
      .create({ to, from, url ,record})
      .then((call) => {
        console.log('Call successfully placed');
        console.log(call.sid);
        // Make sure to only call `callback` once everything is finished, and to pass
        // null as the first parameter to signal successful execution.
        return callback(null, `Success! Call SID: ${call.sid}`);
      })
      .catch((error) => {
        console.error(error);
        return callback(error);
      });
  };
  