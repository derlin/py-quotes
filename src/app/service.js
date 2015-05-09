/**
 *
 * @author: Lucy Linder
 * @date: 07.05.2015
 */

var service = angular.module('quotes.service', ['ngResource']);

var server = "/generator/:id";

service.factory('QuotesFactory', function ($resource){
    return $resource(server, {}, {
        getall: { method: 'GET', params: {id: '@id'}, isArray: true },
        create: { method: 'POST'},
        delete: { method: 'DELETE', params: {id: '@id'}},
        update: { method: 'PUT', params: {id: '@date'}}
        //search: {method: 'search', params: {m: '@m', s: '@s'}}
    })
});
