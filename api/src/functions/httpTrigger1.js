const logging = require('azure-functions-logger');
const azure = require('azure-functions');

module.exports = async function (context, req) {
    logging.info('JavaScript HTTP trigger function processed a request.');

    const name = req.query.name || (req.body && req.body.name);
    if (name) { 
        return {
            status: 200,
            body: `Hello, ${name}!`
        };
    } else {
        return {
            status: 200,
            body: "Hello, world!"
        };
    }
}
    
