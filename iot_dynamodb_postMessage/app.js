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

exports.postMessage = async (event, context) => {
    console.log("postMessage event:", event);

    if (tableName == null) {
        tableName = await getParameter(ssm_param);
    }

    let parsedBody = JSON.parse(event.body);

    params = {
        TableName: tableName.Parameter.Value,
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