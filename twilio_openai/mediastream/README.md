# Readme for Twilio Media Stream

## Prerequisites

Before you start integrating Twilio with ChatGPT, make sure you have the following prerequisites:

1. **Twilio Account:** Sign up for a Twilio account.

2. **Twilio Phone Number:** Obtain a Twilio phone number. You can find instructions on how to get your first Twilio number in your trial account [here](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account#get-your-first-twilio-phone-number).

3. **Twilio CLI with Serverless Toolkit:** Make sure you have the Twilio CLI installed with the Serverless Toolkit. You can install it using the following command:

   ```
   npm install twilio-cli -g
   ```

## Integration Steps

1. Create a `.env` file similar as `.env.example` with your Google Application crediantials (json file) path as `GOOGLE_APPLICATION_CREDENTIALS`. Your `.env` file should look like this (replace `XXXXX` with your respective path of the file):

   ```
   GOOGLE_APPLICATION_CREDENTIALS=XXXXX
   ```


2. Install the WebSocket and Express NPM package as a dependency:

   ```
   npm install ws express
   ```

3. In a new Terminal run this command

    ```
    node index
    ```

   then in another terminal run the command

   ```
   ngrok http 8080
   ```

   then grab the forwarding url and copy it down somewhere and it will be termed as 'NGROK_URL' later in the code

4. Buy a Twilio Phone number using this command

   ```
   twilio phone-numbers:buy:mobile --country-code US
   ```

5. Point your voice url to your ngrok url using the following command:
    Replace TWILIO_PHONE_NUMBER with you twilio phone number and NGROK_URL with your forwarding url

    ```
    twilio phone-numbers:update TWILIO_PHONE_NUMBER --voice-url NGROK_URL
    ```

###    After this step Call your Twilio Phone Number and you will be getting 'Recieving Audio...' in the console

6. Create an application on your [Google Cloud Console](https://console.cloud.google.com/home) to get credentials. 

Download your keys or credentials as json file and store that file in the project folder and after that run the following command:

    ```
    npm install --save @google-cloud/speech
    ```

### Testing

11. Test your integration by making a call to your configured Twilio phone number.

Now your integration is ready to capture spoken input from callers, convert it to text using Google Speech to Text recognition, send it to the console of your code editor. Enjoy your Twilio Transcription Call integration!
