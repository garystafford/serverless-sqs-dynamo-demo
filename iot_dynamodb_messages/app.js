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
                console.log(`getMessages ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });
            } else {
                console.log(`getMessages data=${JSON.stringify(data)}`);
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

    return await new Promise((resolve, reject) => {
        docClient.put(params, (error, data) => {
            if (error) {
                console.log(`postMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not post message: ${error.stack}`
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

exports.putMessage = async (event, context) => {
    console.log("putMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let parsedBody = JSON.parse(event.body);

    params = {
        TableName: tableName,
        Key: {
            "date": parsedBody.Key.date,
            "time": parsedBody.Key.time
        },
        UpdateExpression: parsedBody.UpdateExpression,
        ExpressionAttributeValues: parsedBody.ExpressionAttributeValues

    };
    console.log(params);

    return await new Promise((resolve, reject) => {
        docClient.update(params, (error, data) => {
            if (error) {
                console.log(`putMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not update message: ${error.stack}`
                });
            } else {
                console.log(`putMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 204,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.deleteMessage = async (event, context) => {
    console.log("deleteMessage event:", event);

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
        docClient.delete(params, (error, data) => {
            if (error) {
                console.log(`deleteMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not delete messages: ${error.stack}`
                });
            } else {
                console.log(`deleteMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};