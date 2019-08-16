'use strict';

console.log('Loading function');

let AWS = require("aws-sdk");
let docClient = new AWS.DynamoDB.DocumentClient();
let ssm = new AWS.SSM();
let params;
let ssm_param = {
    Name: '/iot_demo/table_name'
};
let tableName;

async function getParameter(param) {
    return await new Promise(function (resolve, reject) {
        ssm.getParameter(param, function (err, data) {
            if (err) {
                reject(err);
            } else {
                console.log(data);
                resolve(data);
            }
        });
    });
}

exports.getMessages = async (event, context) => {
    console.log("getMessage event:", event);

    if (tableName == null) {
        tableName = await getParameter(ssm_param);
    }

    params = {
        TableName: tableName.Parameter.Value
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
        tableName = await getParameter(ssm_param);
    }
    params = {
        TableName: tableName.Parameter.Value,
        Key: {
            "timestamp": parseFloat(event.pathParameters.timestamp),
            "location": event.queryStringParameters.location
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