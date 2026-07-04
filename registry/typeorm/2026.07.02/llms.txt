# TypeORM

> TypeORM is an ORM that can run in NodeJS, Browser, Cordova, Ionic, React Native, NativeScript, Expo, and Electron platforms and can be used with TypeScript and JavaScript.

- [TypeORM](https://typeorm.io/index.md)

## maintainers

Meet the team behind TypeORM

- [Maintainers](https://typeorm.io/maintainers.md): Meet the team behind TypeORM

## docs


### data-source


#### data-source

What is a DataSource?

- [DataSource](https://typeorm.io/docs/data-source/data-source.md): What is a DataSource?

#### data-source-api

- options - Options used to create this dataSource.

- [DataSource API](https://typeorm.io/docs/data-source/data-source-api.md): - options - Options used to create this dataSource.

#### data-source-options

What is DataSourceOptions?

- [Data Source Options](https://typeorm.io/docs/data-source/data-source-options.md): What is DataSourceOptions?

#### multiple-data-sources

Using multiple data sources

- [Multiple data sources, databases, schemas and replication setup](https://typeorm.io/docs/data-source/multiple-data-sources.md): Using multiple data sources

#### null-and-undefined-handling

In 'WHERE' conditions the values null and undefined are not strictly valid values in TypeORM.

- [Handling null and undefined values in where conditions](https://typeorm.io/docs/data-source/null-and-undefined-handling.md): In 'WHERE' conditions the values null and undefined are not strictly valid values in TypeORM.

### drivers


#### google-spanner

Installation

- [Google Spanner](https://typeorm.io/docs/drivers/google-spanner.md): Installation

#### microsoft-sqlserver

Installation

- [Microsoft SQLServer](https://typeorm.io/docs/drivers/microsoft-sqlserver.md): Installation

#### mongodb

MongoDB support

- [MongoDB](https://typeorm.io/docs/drivers/mongodb.md): MongoDB support

#### mysql

MySQL, MariaDB and Amazon Aurora MySQL are supported as TypeORM drivers.

- [MySQL / MariaDB](https://typeorm.io/docs/drivers/mysql.md): MySQL, MariaDB and Amazon Aurora MySQL are supported as TypeORM drivers.

#### oracle

Installation

- [Oracle](https://typeorm.io/docs/drivers/oracle.md): Installation

#### postgres

PostgreSQL, CockroachDB and Amazon Aurora Postgres are supported as TypeORM drivers.

- [Postgres / CockroachDB](https://typeorm.io/docs/drivers/postgres.md): PostgreSQL, CockroachDB and Amazon Aurora Postgres are supported as TypeORM drivers.

#### sap

Installation

- [SAP HANA](https://typeorm.io/docs/drivers/sap.md): Installation

#### sqlite

Installation

- [SQLite](https://typeorm.io/docs/drivers/sqlite.md): Installation

### entity


#### embedded-entities

There is an amazing way to reduce duplication in your app (using composition over inheritance) by using embedded columns.

- [Embedded Entities](https://typeorm.io/docs/entity/embedded-entities.md): There is an amazing way to reduce duplication in your app (using composition over inheritance) by using embedded columns.

#### entities

What is an Entity?

- [Entities](https://typeorm.io/docs/entity/entities.md): What is an Entity?

#### entity-inheritance

Concrete Table Inheritance

- [Entity Inheritance](https://typeorm.io/docs/entity/entity-inheritance.md): Concrete Table Inheritance

#### separating-entity-definition

Defining Schemas

- [Separating Entity Definition](https://typeorm.io/docs/entity/separating-entity-definition.md): Defining Schemas

#### tree-entities

TypeORM supports the Adjacency list and Closure table patterns for storing tree structures.

- [Tree Entities](https://typeorm.io/docs/entity/tree-entities.md): TypeORM supports the Adjacency list and Closure table patterns for storing tree structures.

#### view-entities

What is a ViewEntity?

- [View Entities](https://typeorm.io/docs/entity/view-entities.md): What is a ViewEntity?

### getting-started

TypeORM is an ORM

- [Getting Started](https://typeorm.io/docs/getting-started.md): TypeORM is an ORM

### guides


#### active-record-data-mapper

What is the Active Record pattern?

- [Active Record vs Data Mapper](https://typeorm.io/docs/guides/active-record-data-mapper.md): What is the Active Record pattern?

#### example-with-express

Initial setup

- [Example using TypeORM with Express](https://typeorm.io/docs/guides/example-with-express.md): Initial setup

#### sequelize-migration

Setting up a data source

- [Migration from Sequelize to TypeORM](https://typeorm.io/docs/guides/sequelize-migration.md): Setting up a data source

#### sql-tag

TypeORM provides a way to write SQL queries using template literals with automatic parameter handling based on your database type. This feature helps prevent SQL injection while making queries more readable. The SQL tag is implemented as a wrapper around the .query method, providing an alternative interface while maintaining the same underlying functionality.

- [SQL Tag](https://typeorm.io/docs/guides/sql-tag.md): TypeORM provides a way to write SQL queries using template literals with automatic parameter handling based on your database type. This feature helps prevent SQL injection while making queries more readable. The SQL tag is implemented as a wrapper around the .query method, providing an alternative interface while maintaining the same underlying functionality.

#### usage-with-javascript

TypeORM can be used not only with TypeScript, but also with JavaScript.

- [Using with JavaScript](https://typeorm.io/docs/guides/usage-with-javascript.md): TypeORM can be used not only with TypeScript, but also with JavaScript.

#### validation

To use validation use class-validator.

- [Using Validation](https://typeorm.io/docs/guides/validation.md): To use validation use class-validator.

### help


#### decorator-reference

Entity decorators

- [Decorator reference](https://typeorm.io/docs/help/decorator-reference.md): Entity decorators

#### faq

How do I update a database schema?

- [FAQ](https://typeorm.io/docs/help/faq.md): How do I update a database schema?

#### support

Found a bug or want to propose a new feature?

- [Support](https://typeorm.io/docs/help/support.md): Found a bug or want to propose a new feature?

#### supported-platforms

NodeJS

- [Supported platforms](https://typeorm.io/docs/help/supported-platforms.md): NodeJS

### indexes

Column indexes

- [Indexes](https://typeorm.io/docs/indexes.md): Column indexes

### listeners-and-subscribers

What is an Entity Listener?

- [Listeners and Subscribers](https://typeorm.io/docs/listeners-and-subscribers.md): What is an Entity Listener?

### logging

Enabling logging

- [Logging](https://typeorm.io/docs/logging.md): Enabling logging

### migrations


#### api

In order to use an API to change a database schema you can use QueryRunner.

- [Query Runner API](https://typeorm.io/docs/migrations/api.md): In order to use an API to change a database schema you can use QueryRunner.

#### creating

You can create a new migration using CLI by specifying the name and location of the migration:

- [Creating manually](https://typeorm.io/docs/migrations/creating.md): You can create a new migration using CLI by specifying the name and location of the migration:

#### executing

Once you have a migration to run on production, you can run them using a CLI command:

- [Executing and reverting](https://typeorm.io/docs/migrations/executing.md): Once you have a migration to run on production, you can run them using a CLI command:

#### extra

Timestamp

- [Extra options](https://typeorm.io/docs/migrations/extra.md): Timestamp

#### faking

You can also fake run a migration using the --fake flag (-f for short). This will add the migration

- [Faking Migrations and Rollbacks](https://typeorm.io/docs/migrations/faking.md): You can also fake run a migration using the --fake flag (-f for short). This will add the migration

#### generating

TypeORM is able to automatically generate migration files based on the changes you made to the entities, comparing them with existing database schema on the server.

- [Generating](https://typeorm.io/docs/migrations/generating.md): TypeORM is able to automatically generate migration files based on the changes you made to the entities, comparing them with existing database schema on the server.

#### reverting

If for some reason you want to revert the changes, you can run:

- [Reverting](https://typeorm.io/docs/migrations/reverting.md): If for some reason you want to revert the changes, you can run:

#### setup

Before working with migrations you need to setup your DataSource options properly:

- [Setup](https://typeorm.io/docs/migrations/setup.md): Before working with migrations you need to setup your DataSource options properly:

#### status

To show all migrations and whether they've been run or not use following command:

- [Status](https://typeorm.io/docs/migrations/status.md): To show all migrations and whether they've been run or not use following command:

#### vite

Using TypeORM in a Vite project is pretty straight forward. However, when you use migrations, you will run into "...migration name is wrong. Migration class name should have a

- [Vite](https://typeorm.io/docs/migrations/vite.md): Using TypeORM in a Vite project is pretty straight forward. However, when you use migrations, you will run into "...migration name is wrong. Migration class name should have a

#### why

Once you get into production you'll need to synchronize model changes into the database.

- [How migrations work?](https://typeorm.io/docs/migrations/why.md): Once you get into production you'll need to synchronize model changes into the database.

### performance-optimization


#### caching

Caching is the technique of temporarily storing query results or data for use in future requests without querying the database each time.

- [Caching](https://typeorm.io/docs/performance-optimization/caching.md): Caching is the technique of temporarily storing query results or data for use in future requests without querying the database each time.

#### efficient-use-of-query-builder

Avoiding the N+1 Query Problem

- [Efficient use of Query Builder](https://typeorm.io/docs/performance-optimization/efficient-use-of-query-builder.md): Avoiding the N+1 Query Problem

#### introduction

In applications using ORM like TypeORM, performance optimization is crucial to ensure the system runs smoothly, minimizes latency, and uses resources efficiently.

- [Introduction](https://typeorm.io/docs/performance-optimization/introduction.md): In applications using ORM like TypeORM, performance optimization is crucial to ensure the system runs smoothly, minimizes latency, and uses resources efficiently.

#### lazy-and-eager-loading

TypeORM provides two main methods for loading data relations: Lazy Loading and Eager Loading. Each has a different impact on the performance of your application.

- [Lazy and Eager Loading](https://typeorm.io/docs/performance-optimization/lazy-and-eager-loading.md): TypeORM provides two main methods for loading data relations: Lazy Loading and Eager Loading. Each has a different impact on the performance of your application.

#### pagination

Pagination is a crucial technique for improving performance when retrieving large amounts of data. Instead of fetching all data at once, pagination divides data into smaller pages, reducing database load and optimizing memory usage.

- [Pagination](https://typeorm.io/docs/performance-optimization/pagination.md): Pagination is a crucial technique for improving performance when retrieving large amounts of data. Instead of fetching all data at once, pagination divides data into smaller pages, reducing database load and optimizing memory usage.

#### query-hints

Query Hints are instructions sent along with SQL queries, helping the database decide on more efficient execution strategies.

- [Query Hints](https://typeorm.io/docs/performance-optimization/query-hints.md): Query Hints are instructions sent along with SQL queries, helping the database decide on more efficient execution strategies.

#### using-indexes

Indexes are data structures that allow the database to locate rows without scanning the entire table. Without an index, a query must examine every row to find matches. With an index, the database can jump directly to the relevant rows — dramatically reducing the number of rows examined.

- [Using indexes](https://typeorm.io/docs/performance-optimization/using-indexes.md): Indexes are data structures that allow the database to locate rows without scanning the entire table. Without an index, a query must examine every row to find matches. With an index, the database can jump directly to the relevant rows — dramatically reducing the number of rows examined.

### query-builder


#### caching

You can cache results selected by these QueryBuilder methods: getMany, getOne, getRawMany, getRawOne and getCount.

- [Caching queries](https://typeorm.io/docs/query-builder/caching.md): You can cache results selected by these QueryBuilder methods: getMany, getOne, getRawMany, getRawOne and getCount.

#### delete-query-builder

Delete

- [Delete using Query Builder](https://typeorm.io/docs/query-builder/delete-query-builder.md): Delete

#### insert-query-builder

You can create INSERT queries using QueryBuilder.

- [Insert using Query Builder](https://typeorm.io/docs/query-builder/insert-query-builder.md): You can create INSERT queries using QueryBuilder.

#### relational-query-builder

RelationQueryBuilder is a special type of QueryBuilder which allows you to work with your relations.

- [Working with Relations](https://typeorm.io/docs/query-builder/relational-query-builder.md): RelationQueryBuilder is a special type of QueryBuilder which allows you to work with your relations.

#### select-query-builder

What is a QueryBuilder?

- [Select using Query Builder](https://typeorm.io/docs/query-builder/select-query-builder.md): What is a QueryBuilder?

#### update-query-builder

You can create UPDATE queries using QueryBuilder.

- [Update using Query Builder](https://typeorm.io/docs/query-builder/update-query-builder.md): You can create UPDATE queries using QueryBuilder.

### query-runner

What is a QueryRunner?

- [Query Runner](https://typeorm.io/docs/query-runner.md): What is a QueryRunner?

### relations


#### eager-and-lazy-relations

Eager relations

- [Eager and Lazy Relations](https://typeorm.io/docs/relations/eager-and-lazy-relations.md): Eager relations

#### many-to-many-relations

What are many-to-many relations?

- [Many-to-many relations](https://typeorm.io/docs/relations/many-to-many-relations.md): What are many-to-many relations?

#### many-to-one-one-to-many-relations

Many-to-one / one-to-many is a relation where A contains multiple instances of B, but B contains only one instance of A.

- [Many-to-one / one-to-many relations](https://typeorm.io/docs/relations/many-to-one-one-to-many-relations.md): Many-to-one / one-to-many is a relation where A contains multiple instances of B, but B contains only one instance of A.

#### one-to-one-relations

One-to-one is a relation where A contains only one instance of B, and B contains only one instance of A.

- [One-to-one relations](https://typeorm.io/docs/relations/one-to-one-relations.md): One-to-one is a relation where A contains only one instance of B, and B contains only one instance of A.

#### relations

What are relations?

- [Relations](https://typeorm.io/docs/relations/relations.md): What are relations?

#### relations-faq

How to create self referencing relation?

- [Relations FAQ](https://typeorm.io/docs/relations/relations-faq.md): How to create self referencing relation?

### releases


#### 1.0

- [Release Notes 1.0](https://typeorm.io/docs/releases/1.0/release-notes.md): TypeORM 1.0 is a major release that removes long-deprecated APIs, modernizes platform requirements, and ships dozens of bug fixes and new features accumulated during the 0.3.x cycle.
- [Upgrading from 0.3 to 1.0](https://typeorm.io/docs/releases/1.0/upgrading-from-0.3.md): This is the upgrading guide from version 0.3.x to 1.0.

#### roadmap

You can track upcoming releases and their progress via GitHub milestones:

- [Roadmap](https://typeorm.io/docs/releases/roadmap.md): You can track upcoming releases and their progress via GitHub milestones:

### transactions

Creating and using transactions

- [Transactions](https://typeorm.io/docs/transactions.md): Creating and using transactions

### using-cli

Installing CLI

- [Using CLI](https://typeorm.io/docs/using-cli.md): Installing CLI

### working-with-entity-manager


#### custom-repository

You can create a custom repository which should contain methods to work with your database.

- [Custom repositories](https://typeorm.io/docs/working-with-entity-manager/custom-repository.md): You can create a custom repository which should contain methods to work with your database.

#### entity-manager-api

- dataSource - The DataSource used by EntityManager.

- [EntityManager API](https://typeorm.io/docs/working-with-entity-manager/entity-manager-api.md): - dataSource - The DataSource used by EntityManager.

#### find-options

Basic options

- [Find Options](https://typeorm.io/docs/working-with-entity-manager/find-options.md): Basic options

#### repository-api

Repository API

- [Repository APIs](https://typeorm.io/docs/working-with-entity-manager/repository-api.md): Repository API

#### working-with-entity-manager

Using EntityManager you can manage (insert, update, delete, load, etc.) any entity.

- [EntityManager](https://typeorm.io/docs/working-with-entity-manager/working-with-entity-manager.md): Using EntityManager you can manage (insert, update, delete, load, etc.) any entity.

#### working-with-repository

Repository is just like EntityManager but its operations are limited to a concrete entity.

- [Repository](https://typeorm.io/docs/working-with-entity-manager/working-with-repository.md): Repository is just like EntityManager but its operations are limited to a concrete entity.
