'use strict';

console.log("Loading function");

let AWS = require("aws-sdk");
let docClient = new AWS.DynamoDB.DocumentClient();
let params;
let tableName;

exports.getMessages = async (event, context) => {
    console.debug("getMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let params = {
        TableName: tableName
    };
    console.debug(params);

    // https://techsparx.com/software-development/aws/aws-sdk-promises.html
    return await new Promise((resolve, reject) => {
        docClient.scan(params, (error, data) => {
            if (error) {
                console.error(`getMessages ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });
            } else {
                console.info(`getMessages data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.getMessage = async (event, context) => {
    console.debug("getMessage event:", event);

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
    console.debug(params.Key);

    return await new Promise((resolve, reject) => {
        docClient.get(params, (error, data) => {
            if (error) {
                console.error(`getMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not get messages: ${error.stack}`
                });
            } else {
                console.info(`getMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.postMessage = async (event, context) => {
    console.debug("postMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let parsedBody = JSON.parse(event.body);

    params = {
        TableName: tableName,
        Item: parsedBody.Item
    };
    console.debug(params);

    return await new Promise((resolve, reject) => {
        docClient.put(params, (error, data) => {
            if (error) {
                console.error(`postMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not post message: ${error.stack}`
                });
            } else {
                console.info(`postMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 201,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.putMessage = async (event, context) => {
    console.debug("putMessage event:", event);

    if (tableName == null) {
        tableName = process.env.TABLE_NAME;
    }

    let parsedBody = JSON.parse(event.body);

    params = {
        TableName: tableName,
        Key: {
            "date": event.pathParameters.date,
            "time": event.queryStringParameters.time
        },
        UpdateExpression: parsedBody.UpdateExpression,
        ExpressionAttributeValues: parsedBody.ExpressionAttributeValues

    };
    console.debug(params);

    return await new Promise((resolve, reject) => {
        docClient.update(params, (error, data) => {
            if (error) {
                console.error(`putMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not update message: ${error.stack}`
                });
            } else {
                console.info(`putMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 204,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};

exports.deleteMessage = async (event, context) => {
    console.debug("deleteMessage event:", event);

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
    console.debug(params.Key);

    return await new Promise((resolve, reject) => {
        docClient.delete(params, (error, data) => {
            if (error) {
                console.error(`deleteMessage ERROR=${error.stack}`);
                resolve({
                    statusCode: 400,
                    error: `Could not delete messages: ${error.stack}`
                });
            } else {
                console.info(`deleteMessage data=${JSON.stringify(data)}`);
                resolve({
                    statusCode: 200,
                    body: JSON.stringify(data)
                });
            }
        });
    });
};