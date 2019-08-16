'use strict';

console.log("Loading function");

let AWS = require("aws-sdk");
let docClient = new AWS.DynamoDB.DocumentClient();
let params;
let tableName;

exports.getMessages = async (event, context) => {
    console.log("getMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let params = {
        TableName: tableName
    };
    console.log(params);

    // https://techsparx.com/software-development/aws/aws-sdk-promises.html
    return await new Promise((resolve, reject) => {
        docClient.scan(params, (error, data) => {
            if (error) {
                console.log(`getMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });

            } else {
                console.log(`getMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.getMessage = async (event, context) => {
    console.log("getMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }
    params = {
        TableName: tableName,
        Key: {
            "date": event.pathParameters.date,
            "time": event.queryStringParameters.time
        }
    };
    console.info(params.Key);

    return await new Promise((resolve, reject) => {
        docClient.get(params, (error, data) => {
            if (error) {
                console.log(`getMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });

            } else {
                console.log(`getMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.postMessage = async (event, context) => {
    console.log("postMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let parsedBody = JSON.parse(event.body);

    params = {
        TableName: tableName,
        Item: parsedBody.Item
    };
    console.log(params);

    // https://techsparx.com/software-development/aws/aws-sdk-promises.html
    return await new Promise((resolve, reject) => {
        docClient.put(params, (error, data) => {
            if (error) {
                console.log(`postMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });

            } else {
                console.log(`postMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 201,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};