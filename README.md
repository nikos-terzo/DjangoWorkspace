# Car KM

## Description

This is a small [Django](https://www.djangoproject.com/) project for tracking mainly fuel consumption.

User is able to add her cars and add records to them.

Records have to include kilometres of the car and the date of record.

FuelRecords describe a fuel refill event with the price of the fuel, the quantity refilled, the total price and the type of the fuel.

FuelRecords can also include the gas station of the refill.

Records in general have also a comments section (RichRecords) as a fast implementation for other kind of records (oil change, service etc.).

## Django-Guardian

This django application runs for users created via the admin page, but user registration is in the TODO list.

[Django-Guardian](https://github.com/django-guardian/django-guardian) is used to support user-object permissions.

Specifically, a user cannot see any car of a group she doesn't belong to and cannot change an object she didn't add;
but can add a record of a car in her group and use resources created by another user in her group.