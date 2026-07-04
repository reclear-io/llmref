---
url: 'https://elysiajs.com/plugins/graphql-apollo.md'
---

# GraphQL Apollo Plugin

Plugin for [elysia](https://github.com/elysiajs/elysia) for using GraphQL Apollo.

Install with:

```bash
bun add graphql @elysia/apollo @apollo/server
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { apollo, gql } from '@elysia/apollo'

const app = new Elysia()
	.use(
		apollo({
			typeDefs: gql`
				type Book {
					title: String
					author: String
				}

				type Query {
					books: [Book]
				}
			`,
			resolvers: {
				Query: {
					books: () => {
						return [
							{
								title: 'Elysia',
								author: 'saltyAom'
							}
						]
					}
				}
			}
		})
	)
	.listen(3000)
```

Accessing `/graphql` should show the Apollo GraphQL playground to work with.

## Context

Because Elysia is based on Web Standard Request and Response which is different from Node's `HttpRequest` and `HttpResponse` that Express uses, results in `req, res` being undefined in context.

Because of this, Elysia replaces both with `context` like route parameters.

```typescript
const app = new Elysia()
	.use(
		apollo({
			typeDefs,
			resolvers,
			context: async ({ request }) => {
				const authorization = request.headers.get('Authorization')

				return {
					authorization
				}
			}
		})
	)
	.listen(3000)
```

## Config

This plugin extends Apollo's [ServerRegistration](https://www.apollographql.com/docs/apollo-server/api/apollo-server/#options) (which is `ApolloServer`'s' constructor parameter).

Below are the extended parameters for configuring Apollo Server with Elysia.

### path

@default `"/graphql"`

Path to expose Apollo Server.

### enablePlayground

@default `process.env.ENV !== 'production'`

Determine whether Apollo should provide Apollo Playground.

---

---
url: 'https://elysiajs.com/at-glance.md'
---

# At a glance

Elysia is an ergonomic web framework for building backend servers with Bun.

Designed with simplicity and type-safety in mind, Elysia offers a familiar API with extensive support for TypeScript and is optimized for Bun.

Here's a simple hello world in Elysia.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', 'Hello Elysia')
    .get('/user/:id', ({ params: { id }}) => id)
    .post('/form', ({ body }) => body)
    .listen(3000)
```

Navigate to [localhost:3000](http://localhost:3000/) and you should see 'Hello Elysia' as the result.

::: tip
Hover over the code snippet to see the type definition.

In the mock browser, click on the path highlighted in blue to change paths and preview the response.

Elysia can run in the browser, and the results you see are actually executed using Elysia.
:::

## Performance

Building on Bun and extensive optimization like static code analysis allows Elysia to generate optimized code on the fly.

Elysia can outperform most web frameworks available today\[1], and even match the performance of Golang and Rust frameworks\[2].

| Framework     | Runtime | Average     | Plain Text | Dynamic Parameters | JSON Body  |
| ------------- | ------- | ----------- | ---------- | ------------------ | ---------- |
| bun           | bun     | 262,660.433 | 326,375.76 | 237,083.18         | 224,522.36 |
| elysia        | bun     | 255,574.717 | 313,073.64 | 241,891.57         | 211,758.94 |
| hyper-express | node    | 234,395.837 | 311,775.43 | 249,675            | 141,737.08 |
| hono          | bun     | 203,937.883 | 239,229.82 | 201,663.43         | 170,920.4  |
| h3            | node    | 96,515.027  | 114,971.87 | 87,935.94          | 86,637.27  |
| oak           | deno    | 46,569.853  | 55,174.24  | 48,260.36          | 36,274.96  |
| fastify       | bun     | 65,897.043  | 92,856.71  | 81,604.66          | 23,229.76  |
| fastify       | node    | 60,322.413  | 71,150.57  | 62,060.26          | 47,756.41  |
| koa           | node    | 39,594.14   | 46,219.64  | 40,961.72          | 31,601.06  |
| express       | bun     | 29,715.537  | 39,455.46  | 34,700.85          | 14,990.3   |
| express       | node    | 15,913.153  | 17,736.92  | 17,128.7           | 12,873.84  |

## TypeScript

Elysia is designed to help you write less TypeScript.

Elysia's Type System is fine-tuned to infer types from your code automatically, without needing to write explicit TypeScript, while providing type-safety at both runtime and compile time for the most ergonomic developer experience.

Take a look at this example:

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .get('/user/:id', ({ params: { id } }) => id)
                        // ^?
    .listen(3000)
```

The above code creates a path parameter **"id"**. The value that replaces `:id` will be passed to `params.id` both at runtime and in types, without manual type declaration.

Elysia's goal is to help you write less TypeScript and focus more on business logic. Let the framework handle the complex types.

TypeScript is not required to use Elysia, but it's recommended.

## Type Integrity

To take it a step further, Elysia provides **Elysia.t**, a schema builder to validate types and values at both runtime and compile time, creating a single source of truth for your data types.

Let's modify the previous code to accept only a number value instead of a string.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/user/:id', ({ params: { id } }) => id, {
                                // ^?
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
```

This code ensures that our path parameter **id** will always be a number at both runtime and compile time (type-level).

::: tip
Hover over "id" in the above code snippet to see a type definition.
:::

With Elysia's schema builder, we can ensure type safety like a strongly typed language with a single source of truth.

## Standard Schema

Elysia supports [Standard Schema](https://github.com/standard-schema/standard-schema), allowing you to use your favorite validation library:

* Zod
* Valibot
* ArkType
* Effect Schema
* Yup
* Joi
* [and more](https://github.com/standard-schema/standard-schema)

```typescript twoslash
import { Elysia } from 'elysia'
import { z } from 'zod'
import * as v from 'valibot'

new Elysia()
	.get('/id/:id', ({ params: { id }, query: { name } }) => id, {
	//                           ^?
		params: z.object({
			id: z.coerce.number()
		}),
		query: v.object({
			name: v.literal('Lilith')
		})
	})
	.listen(3000)
```

Elysia will infer the types from the schema automatically, allowing you to use your favorite validation library while still maintaining type safety.

## OpenAPI

Elysia adopts many standards by default, like OpenAPI, WinterTC compliance, and Standard Schema. Allowing you to integrate with most of the industry standard tools or at least easily integrate with tools you are familiar with.

For instance, because Elysia adopts OpenAPI by default, generating API documentation is as easy as adding a one-liner:

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
    .use(openapi()) // [!code ++]
    .get('/user/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
```

With the OpenAPI plugin, you can seamlessly generate an API documentation page without additional code or specific configuration and share it with your team effortlessly.

## OpenAPI from types

Elysia also supports OpenAPI schema generation with **1 line directly from types**.

This is a **unique feature** of Elysia, allowing you to have complete and accurate API documentation directly from your code without any manual annotation.

```typescript
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi'

export const app = new Elysia()
    .use(openapi({
    	references: fromTypes() // [!code ++]
    }))
    .get('/user/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
```

This is equivalent to **FastAPI**'s automatic OpenAPI generation from types but in TypeScript.

## End-to-end Type Safety

With Elysia, type safety is not limited to server-side.

With Elysia, you can synchronize your types with your frontend team automatically, similar to tRPC, using Elysia's client library, "Eden".

```typescript
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi'

export const app = new Elysia()
    .use(openapi({
    	references: fromTypes()
    }))
    .get('/user/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]
```

And on your client-side:

```typescript twoslash
// @filename: server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/user/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)

export type App = typeof app

// @filename: client.ts
// ---cut---
// client.ts
import { treaty } from '@elysia/eden'
import type { App } from './server'

const app = treaty<App>('localhost:3000')

// Get data from /user/617
const { data } = await app.user({ id: 617 }).get()
      // ^?

console.log(data)
```

With Eden, you can use the existing Elysia types to query an Elysia server **without code generation** and synchronize types for both frontend and backend automatically.

Elysia is not only about helping you create a confident backend but for all that is beautiful in this world.

## Type Soundness

Most frameworks with end-to-end type safety usually assume only a happy part, leaving error handling and edge cases out of the type system.

However, Elysia can infers all of the possible outcomes of your API, from lifecycle events/macro from any part of your codebase.

::: code-group

```typescript twoslash [client.ts]
// @filename: server.ts
import { Elysia, t } from 'elysia'

const plugin = new Elysia()
	.macro({
		auth: {
			cookie: t.Object({
				session: t.String()
			}),
			beforeHandle({ cookie: { session }, status }) {
				if(session.value !== 'valid')
					return status(401)
			}
		}
	})

const app = new Elysia()
	.use(plugin)
    .get('/user/:id', ({ params: { id }, status }) => {
    	if(Math.random() > 0.1)
     		return status(420)
       
       return id
    }, {
    	auth: true,
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)

export type App = typeof app

// @filename: client.ts
// ---cut---
// client.ts
import { treaty } from '@elysia/eden'
import type { App } from './server'

const app = treaty<App>('localhost:3000')

// Get data from /user/617
const { data, error } = await app.user({ id: 617 }).get()
            // ^?




















console.log(data)
```

```typescript [server.ts]
import { Elysia, t } from 'elysia'

const plugin = new Elysia()
	.macro({
		auth: {
			cookie: t.Object({
				session: t.String()
			}),
			beforeHandle({ cookie: { session }, status }) {
				if(session.value !== 'valid')
					return status(401)
			}
		}
	})

const app = new Elysia()
	.use(plugin)
    .get('/user/:id', ({ params: { id }, status }) => {
    	if(Math.random() > 0.1)
     		return status(420)
       
       return id
    }, {
    	auth: true,
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
    
export type App = typeof app
```

:::

This is one of the **unfair advantages** that Elysia has from years of investment in type system.

## Platform Agnostic

Elysia is optimized for Bun with native feature but **not limited to Bun**.

Being [WinterTC compliant](https://wintertc.org/) allows you to deploy Elysia servers on:

* Bun
* [Node.js](/integrations/node)
* [Deno](/integrations/deno)
* [Cloudflare Worker](/integrations/cloudflare-worker)
* [Vercel](/integrations/vercel)
* [Expo](/integrations/expo) via API routes
* [Nextjs](/integrations/nextjs) via API routes
* [Astro](/integrations/astro) via API routes

and several more! Checkout `integration` section on sidebar for more support runtime.

## Our Community

We want to create a friendly and welcoming community for everyone with bright, cute, friendly and playful design including our hand drawn anime girl mascot, *"Elysia chan"*.

We believe that technology should be friendly and approachable instead of being serious all the time, to brings joy to people's lives.

But even that, **we take Elysia very seriously** to make sure it's reliable and production ready high-performance framework that can be trusted for your next project.

Elysia is **used in production by many companies and projects worldwide**, including [X](https://x.com/shlomiatar/status/1822381556142362734), [Bank for Agriculture and Agricultural Co-operatives](https://github.com/elysiajs/elysia/discussions/1312#discussioncomment-13924470), [Cluely](https://github.com/elysiajs/elysia/discussions/1312#discussioncomment-14420139), [CS.Money](https://github.com/elysiajs/elysia/discussions/1312#discussioncomment-13913513), [Abacate Pay](https://github.com/elysiajs/elysia/discussions/1312#discussioncomment-13922081) and used by [over 10,000 (open source) projects on GitHub.](https://github.com/elysiajs/elysia/network/dependents) and has been actively developed and maintained since 2022 with many regular contributors from our community.

Elysia is a reliable choice and production ready for building your next backend server.

Here's on of our community resources to get you started:

***

1\. Measured in requests/second. The benchmark for parsing query, path parameter and set response header on Debian 11, Intel i7-13700K tested on Bun 0.7.2 on 6 Aug 2023. See the benchmark condition [here](https://github.com/SaltyAom/bun-http-framework-benchmark/tree/c7e26fe3f1bfee7ffbd721dbade10ad72a0a14ab#results).

2\. Based on [TechEmpower Benchmark round 22](https://www.techempower.com/benchmarks/#section=data-r22\&hw=ph\&test=composite).

---

---
url: 'https://elysiajs.com/plugins/bearer.md'
---

# Bearer Plugin

Plugin for [elysia](https://github.com/elysiajs/elysia) for retrieving the Bearer token.

Install with:

```bash
bun add @elysia/bearer
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { bearer } from '@elysia/bearer'

const app = new Elysia()
    .use(bearer())
    .get('/sign', ({ bearer }) => bearer, {
        beforeHandle({ bearer, set, status }) {
            if (!bearer) {
                set.headers[
                    'WWW-Authenticate'
                ] = `Bearer realm='sign', error="invalid_request"`

                return status(400, 'Unauthorized')
            }
        }
    })
    .listen(3000)
```

This plugin is for retrieving a Bearer token specified in [RFC6750](https://www.rfc-editor.org/rfc/rfc6750#section-2).

This plugin DOES NOT handle authentication validation for your server. Instead, the plugin leaves the decision to developers to apply the logic for handling validation checks themselves.

---

---
url: 'https://elysiajs.com/essential/best-practice.md'
---

# Best Practice

Elysia is a pattern-agnostic framework, leaving the decision of which coding patterns to use up to you and your team.

However, there are several concerns when trying to adapt an MVC pattern [(Model-View-Controller)](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) with Elysia, and we found it hard to decouple and handle types.

This page is a guide on how to follow Elysia structure best practices combined with the MVC pattern, but it can be adapted to any coding pattern you prefer.

## Folder Structure

Elysia is unopinionated about folder structure, leaving you to **decide** how to organize your code yourself.

However, **if you don't have a specific structure in mind**, we recommend a feature-based folder structure where each feature has its own folder containing controllers, services, and models.

```
| src
  | modules
	| auth
	  | index.ts (Elysia controller)
	  | service.ts (service)
	  | model.ts (model)
	| user
	  | index.ts (Elysia controller)
	  | service.ts (service)
	  | model.ts (model)
  | utils
	| a
	  | index.ts
	| b
	  | index.ts
```

This structure allows you to easily find and manage your code and keep related code together.

Here's an example code of how to distribute your code into a feature-based folder structure:

::: code-group

```typescript [auth/index.ts]
import { Elysia } from 'elysia'

import { Auth } from './service'
import { AuthModel } from './model'

export const auth = new Elysia({ prefix: '/auth' })
	.get(
		'/sign-in',
		async ({ body, cookie: { session } }) => {
			const response = await Auth.signIn(body)

			// Set session cookie
			// (Elysia cookie is proxy, it can never be null/undefined)
			session!.value = response.token

			return response
		}, {
			body: AuthModel.signInBody,
			// response is optional, use to enforce return type
			response: {
				200: AuthModel.signInResponse,
				400: AuthModel.signInInvalid
			}
		}
	)
```

```typescript [auth/service.ts]
// Service handles business logic, decoupled from Elysia controller
import { status } from 'elysia'

import type { AuthModel } from './model'

// If a class doesn't need to store a property,
// you can use an `abstract class` to avoid class allocation
export abstract class Auth {
	static async signIn({ username, password }: AuthModel['signInBody']) {
		const user = await sql`
			SELECT password
			FROM users
			WHERE username = ${username}
			LIMIT 1`

		if (!await Bun.password.verify(password, user.password))
			// You can throw an HTTP error directly
			throw status(
				400,
				'Invalid username or password' satisfies AuthModel['signInInvalid']
			)

		return {
			username,
			token: await generateAndSaveTokenToDB(user.id)
		}
	}
}
```

```typescript [auth/model.ts]
// Model define the data structure and validation for the request and response
import { t, type UnwrapSchema } from 'elysia'

export const AuthModel = {
	signInBody: t.Object({
		username: t.String(),
		password: t.String(),
	}),
	signInResponse: t.Object({
		username: t.String(),
		token: t.String(),
	}),
	signInInvalid: t.Literal('Invalid username or password')
} as const

// Optional, cast all model to TypeScript type
export type AuthModel = {
	[k in keyof typeof AuthModel]: UnwrapSchema<typeof AuthModel[k]>
}
```

:::

Each file has its own responsibility:

* **Controller**: Handles HTTP routing, request validation, and cookies.
* **Service**: Handles business logic, decoupled from the Elysia controller if possible.
* **Model**: Defines the data structure and validation for the request and response.

Feel free to adapt this structure to your needs and use any coding pattern you prefer.

::: note
You may get a warning when using `cookie.name` as it might be `undefined` depending on your TypeScript configuration.

Elysia cookie can never be `undefined` because it's a Proxy object. `cookie` is always defined, only its value (via cookie.value) can be undefined.

This can be fixed by using a \[cookie schema] or disable [strictNullChecks](https://www.typescriptlang.org/tsconfig/#strictNullChecks) in `tsconfig.json`
:::

## Controller

Due to the type soundness of Elysia, it's not recommended to use a traditional controller class that is tightly coupled with Elysia's `Context` because:

1. **Elysia types are complex** and heavily depend on plugins and multiple levels of chaining.
2. **Hard to type**; Elysia types could change at any time, especially with decorators and store.
3. **Loss of type integrity** and inconsistency between types and runtime code.

We recommend one of the following approaches to implement a controller in Elysia.

1. Use Elysia instance as a controller itself
2. Create a controller that is not tied with HTTP request or Elysia.

***

### 1. Elysia instance as a controller

> 1 Elysia instance = 1 controller

Treat an Elysia instance as a controller, and define your routes directly on the Elysia instance.

```typescript
// ✅ Do
import { Elysia } from 'elysia'
import { Service } from './service'

new Elysia()
    .get('/', ({ stuff }) => {
        Service.doStuff(stuff)
    })
```

This approach allows Elysia to infer the `Context` type automatically, ensuring type integrity and consistency between types and runtime code.

```typescript
// ❌ Don't
import { Elysia, t, type Context } from 'elysia'

abstract class Controller {
    static root(context: Context) {
        return Service.doStuff(context.stuff)
    }
}

new Elysia()
    .get('/', Controller.root)
```

This approach makes it hard to type `Context` properly, and may lead to loss of type integrity.

### 2. Controller without HTTP request

If you want to create a controller class, we recommend creating a class that is not tied to HTTP request or Elysia at all.

This approach allows you to decouple the controller from Elysia, making it easier to test, reuse, and even swap a framework while still following the MVC pattern.

```typescript
import { Elysia } from 'elysia'

abstract class Controller {
	static doStuff(stuff: string) {
		return Service.doStuff(stuff)
	}
}

new Elysia()
	.get('/', ({ stuff }) => Controller.doStuff(stuff))
```

Tying the controller to the Elysia Context may lead to:

1. Loss of type integrity
2. Making it harder to test and reuse
3. Vendor lock-in

We recommend keeping the controller decoupled from Elysia as much as possible.

### ❌ Don't: Pass entire `Context` to a controller

**Context is a highly dynamic type** that can be inferred from Elysia instance.

Do not pass an entire `Context` to a controller, instead use object destructuring to extract what you need and pass it to the controller.

```typescript
import type { Context } from 'elysia'

abstract class Controller {
	constructor() {}

	// ❌ Don't do this
	static root(context: Context) {
		return Service.doStuff(context.stuff)
	}
}
```

This approach makes it hard to type `Context` properly, and may lead to loss of type integrity.

### Testing

If you're using Elysia as a controller, you can test your controller using `handle` to directly call a function (and it's lifecycle)

```typescript
import { Elysia } from 'elysia'
import { Service } from './service'

import { describe, it, expect } from 'bun:test'

const app = new Elysia()
    .get('/', ({ stuff }) => {
        Service.doStuff(stuff)

        return 'ok'
    })

describe('Controller', () => {
	it('should work', async () => {
		const response = await app
			.handle(new Request('http://localhost/'))
			.then((x) => x.text())

		expect(response).toBe('ok')
	})
})
```

You may find more information about testing in [Unit Test](/patterns/unit-test.html).

## Service

A service is a set of utility/helper functions decoupled as business logic to use in a module/controller, in our case, an Elysia instance.

Any technical logic that can be decoupled from controller may live inside a **Service**.

There are 2 types of service in Elysia:

1. Non-request dependent service
2. Request dependent service

### 1. Abstract away Non-request dependent service

We recommend abstracting service classes/functions away from Elysia.

If the service or function isn't tied to an HTTP request or doesn't access a `Context`, it's recommended to implement it as a static class or function.

```typescript
import { Elysia, t } from 'elysia'

abstract class Service {
    static fibo(number: number): number {
        if(number < 2)
            return number

        return Service.fibo(number - 1) + Service.fibo(number - 2)
    }
}

new Elysia()
    .get('/fibo', ({ body }) => {
        return Service.fibo(body)
    }, {
        body: t.Numeric()
    })
```

If your service doesn't need to store a property, you can use an `abstract class` and `static` methods to avoid allocating a class instance.

### 2. Request dependent service as Elysia instance

**If the service is a request-dependent service** or needs to process HTTP requests, we recommend abstracting it as an Elysia instance to ensure type integrity and inference:

```typescript
import { Elysia } from 'elysia'

// ✅ Do
const AuthService = new Elysia({ name: 'Auth.Service' })
    .macro({
        isSignIn: {
            resolve({ cookie, status }) {
                if (!cookie.session.value)
                	return status(401, 'Unauthorized')

                return {
                	session: cookie.session.value,
                }
            }
        }
    })

const UserController = new Elysia()
    .use(AuthService)
    .get('/profile', ({ Auth: { user } }) => user, {
    	isSignIn: true
    })
```

::: tip
Elysia handles [plugin deduplication](/essential/plugin.html#plugin-deduplication) by default, so you don't have to worry about performance, as it will be a singleton if you specify a **"name"** property
:::

### ✅ Do: Decorate only request dependent property

It's recommended to `decorate` only for request-dependent properties, such as `requestIP`, `requestTime`, or `session`.

Overusing decorators ties your code to Elysia, making it harder to test and reuse.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.decorate('requestIP', ({ request }) => request.headers.get('x-forwarded-for') || request.ip)
	.decorate('requestTime', () => Date.now())
	.decorate('session', ({ cookie }) => cookie.session.value)
	.get('/', ({ requestIP, requestTime, session }) => {
		return { requestIP, requestTime, session }
	})
```

## Model

Models or [DTOs (Data Transfer Objects)](https://en.wikipedia.org/wiki/Data_transfer_object) are handled by [Elysia.t (Validation)](/essential/validation.html#elysia-type).

Elysia has a built-in validation system that can infer types from your code and validate them at runtime.

### ✅ Do: Use Elysia's validation system

Elysia's strength is prioritizing a single source of truth for both types and runtime validation.

Instead of declaring an interface, reuse validation's model instead:

```typescript twoslash
// ✅ Do
import { Elysia, t, type UnwrapSchema } from 'elysia'

export const models = {
	customBody: t.Object({
		username: t.String(),
		password: t.String()
	})
}

// Optional if you want to extract the type from the model
type CustomBody = UnwrapSchema<typeof models.customBody>
//    ^?






// Or make the entire object as type
type Models = {
	[k in keyof typeof models]: UnwrapSchema<typeof models[k]>
}

// ❌ Don't: declare model and type separately
interface ICustomBody {
	username: string
	password: string
}
```

We can get type of model by using `typeof` with `.static` property from the model.

Then you can use the `CustomBody` type to infer the type of the request body.

```typescript twoslash
import { Elysia, t } from 'elysia'

const models = {
	customBody: t.Object({
		username: t.String(),
		password: t.String()
	})	
}
// ---cut---
// ✅ Do
new Elysia()
	.post('/login', ({ body }) => {
	                 // ^?
		return body
	}, {
		body: models.customBody
	})
```

### ❌ Don't: Declare a class instance as a model

Do not declare a class instance as a model:

```typescript
// ❌ Don't
class CustomBody {
	username: string
	password: string

	constructor(username: string, password: string) {
		this.username = username
		this.password = password
	}
}

// ❌ Don't
interface ICustomBody {
	username: string
	password: string
}
```

### Group

You can group multiple models into a single object to make it more organized.

```typescript
import { Elysia, t } from 'elysia'

export const AuthModel = {
	sign: t.Object({
		username: t.String(),
		password: t.String()
	})
}

const models = AuthModel.models
```

### Model Injection

Though this is optional, if you are strictly following MVC pattern, you may want to inject like a service into a controller. We recommended using [Elysia reference model](/essential/validation#reference-model)

Using Elysia's model reference

```typescript twoslash
import { Elysia, t } from 'elysia'

const customBody = t.Object({
	username: t.String(),
	password: t.String()
})

const AuthModel = new Elysia()
    .model({
        sign: customBody
    })

const models = AuthModel.models

const UserController = new Elysia({ prefix: '/auth' })
    .use(AuthModel)
    .prefix('model', 'auth.')
    .post('/sign-in', async ({ body, cookie: { session } }) => {
                             // ^?

        return true
    }, {
        body: 'auth.Sign'
    })
```

This approach provides several benefits:

1. Allows you to name a model and provide auto-completion.
2. Modifies schemas for later usage, or performs a [remap](/essential/handler.html#remap).
3. Shows up as "models" in OpenAPI-compliant clients, eg. OpenAPI.
4. Improves TypeScript inference speed as model types will be cached during registration.

---

---
url: 'https://elysiajs.com/integrations/better-auth.md'
---

# Better Auth

Better Auth is framework-agnostic authentication (and authorization) framework for TypeScript.
It provides a comprehensive set of features out of the box and includes a plugin ecosystem that simplifies adding advanced functionalities.
We recommend going through the [Better Auth basic setup](https://www.better-auth.com/docs/installation) before going through this page.
Our basic setup will look like this:

```ts [auth.ts]
import { betterAuth } from 'better-auth'
import { Pool } from 'pg'
export const auth = betterAuth({
    database: new Pool()
})
```

## Handler

After setting up the Better Auth instance, we can mount it to Elysia via [mount](/patterns/mount.html).
We need to mount the handler to an Elysia endpoint.

```ts [index.ts]
import { Elysia } from 'elysia'
import { auth } from './auth'
const app = new Elysia()
	.mount(auth.handler) // [!code ++]
	.listen(3000)
console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

Then we can access Better Auth at `http://localhost:3000/api/auth`.

### Custom endpoint

We recommend setting a prefix path when using [mount](/patterns/mount.html).

```ts [index.ts]
import { Elysia } from 'elysia'
const app = new Elysia()
	.mount('/auth', auth.handler) // [!code ++]
	.listen(3000)
console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

Then we can access Better Auth at `http://localhost:3000/auth/api/auth`.
But the URL looks redundant, so we can customize the `/api/auth` prefix to something else in the Better Auth instance.

```ts
import { betterAuth } from 'better-auth'
import { Pool } from 'pg'
export const auth = betterAuth({
    basePath: '/api' // [!code ++]
})
```

Then we can access Better Auth at `http://localhost:3000/auth/api`.
Unfortunately, we can't set the `basePath` of a Better Auth instance to be empty or `/`.

## OpenAPI

Better Auth supports `openapi` with `better-auth/plugins`.
However, if we are using [@elysia/openapi](/plugins/openapi), you might want to extract the documentation from the Better Auth instance.
First, we need to add the `openAPI` plugin to our Better Auth instance:

```ts [auth.ts]
import { betterAuth } from 'better-auth'
import { openAPI } from 'better-auth/plugins' // [!code ++]
import { Pool } from 'pg'
export const auth = betterAuth({
    database: new Pool(),
    plugins: [openAPI()] // [!code ++]
})
```

::: tip
The `openAPI()` plugin is required for `auth.api.generateOpenAPISchema` to be available. Without it, you will get a type error: `Property 'generateOpenAPISchema' does not exist`.
:::
Then we may extract the OpenAPI schema with the following code:

```ts [auth.ts]
let _schema: ReturnType<typeof auth.api.generateOpenAPISchema>
const getSchema = async () => (_schema ??= auth.api.generateOpenAPISchema())
export const OpenAPI = {
    getPaths: (prefix = '/auth/api') =>
        getSchema().then(({ paths }) => {
            const reference: typeof paths = Object.create(null)
            for (const path of Object.keys(paths)) {
                const key = prefix + path
                reference[key] = paths[path]
                for (const method of Object.keys(paths[path])) {
                    const operation = (reference[key] as any)[method]
                    operation.tags = ['Better Auth']
                }
            }
            return reference
        }) as Promise<any>,
    components: getSchema().then(({ components }) => components) as Promise<any>
} as const
```

Then in our Elysia instance that uses `@elysia/openapi`.

```ts
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'
import { OpenAPI } from './auth'
const app = new Elysia().use(
    openapi({
        documentation: {
            components: await OpenAPI.components,
            paths: await OpenAPI.getPaths()
        }
    })
)
```

## CORS

To configure CORS, you can use the `cors` plugin from `@elysia/cors`.

```ts
import { Elysia } from 'elysia'
import { cors } from '@elysia/cors'
import { auth } from './auth'
const app = new Elysia()
    .use(
        cors({
            origin: 'http://localhost:3001',
            methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            credentials: true,
            allowedHeaders: ['Content-Type', 'Authorization']
        })
    )
    .mount(auth.handler)
    .listen(3000)
console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

## Macro

You can use [macro](https://elysiajs.com/patterns/macro.html#macro) with [resolve](https://elysiajs.com/patterns/macro#resolve) to provide session and user information before passing to the view.

```ts
import { Elysia } from 'elysia'
import { auth } from './auth'
// user middleware (compute user and session and pass to routes)
const betterAuth = new Elysia({ name: 'better-auth' })
    .mount(auth.handler)
    .macro({
        auth: {
            async resolve({ status, request: { headers } }) {
                const session = await auth.api.getSession({
                    headers
                })
                if (!session) return status(401)
                return {
                    user: session.user,
                    session: session.session
                }
            }
        }
    })
const app = new Elysia()
    .use(betterAuth)
    .get('/user', ({ user }) => user, {
        auth: true
    })
    .listen(3000)
console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

This will allow you to access the `user` and `session` objects in all of your routes.

---

---
url: 'https://elysiajs.com/integrations/cheat-sheet.md'
---

# Cheat Sheet

Here is a quick overview of common Elysia patterns

## Hello World

A simple hello world

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', () => 'Hello World')
    .listen(3000)
```

## Custom HTTP Method

Define routes using custom HTTP methods/verbs

See [Route](/essential/route.html#custom-method)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/hi', () => 'Hi')
    .post('/hi', () => 'From Post')
    .put('/hi', () => 'From Put')
    .route('M-SEARCH', '/hi', () => 'Custom Method')
    .listen(3000)
```

## Path Parameter

Using dynamic path parameters

See [Path](/essential/route.html#path-type)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id)
    .get('/rest/*', () => 'Rest')
    .listen(3000)
```

## Return JSON

Elysia converts response to JSON automatically

See [Handler](/essential/handler.html)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/json', () => {
        return {
            hello: 'Elysia'
        }
    })
    .listen(3000)
```

## Return a file

A file can be returned as a formdata response

The response must be a 1-level deep object

```typescript
import { Elysia, file } from 'elysia'

new Elysia()
    .get('/json', () => {
        return {
            hello: 'Elysia',
            image: file('public/cat.jpg')
        }
    })
    .listen(3000)
```

## Header and status

Set a custom header and a status code

See [Handler](/essential/handler.html)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ set, status }) => {
        set.headers['x-powered-by'] = 'Elysia'

        return status(418, "I'm a teapot")
    })
    .listen(3000)
```

## Group

Define a prefix once for subroutes

See [Group](/essential/route.html#group)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get("/", () => "Hi")
    .group("/auth", app => {
        return app
            .get("/", () => "Hi")
            .post("/sign-in", ({ body }) => body)
            .put("/sign-up", ({ body }) => body)
    })
    .listen(3000)
```

## Schema

Enforce a data type on a route

See [Validation](/essential/validation)

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .post('/mirror', ({ body: { username } }) => username, {
        body: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
    .listen(3000)
```

## File upload

See [Validation#file](/essential/validation#file)

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/body', ({ body }) => body, {
		body: t.Object({
			file: t.File({ format: 'image/*' }),
			multipleFiles: t.Files()
		})
	})
	.listen(3000)
```

## Lifecycle Hook

Intercept Elysia events in order

See [Lifecycle](/essential/life-cycle.html)

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .onRequest(() => {
        console.log('On request')
    })
    .on('beforeHandle', () => {
        console.log('Before handle')
    })
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            username: t.String(),
            password: t.String()
        }),
        afterHandle: () => {
            console.log("After handle")
        }
    })
    .listen(3000)
```

## Guard

Enforce a data type on subroutes

See [Scope](/essential/plugin.html#scope)

```typescript twoslash
// @errors: 2345
import { Elysia, t } from 'elysia'

new Elysia()
    .guard({
        response: t.String()
    }, (app) => app
        .get('/', () => 'Hi')
        // Invalid: will throws error, and TypeScript will report error
        .get('/invalid', () => 1)
    )
    .listen(3000)
```

## Custom context

Add custom variables to route context

See [Context](/essential/handler.html#context)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .state('version', 1)
    .decorate('getDate', () => Date.now())
    .get('/version', ({
        getDate,
        store: { version }
    }) => `${version} ${getDate()}`)
    .listen(3000)
```

## Redirect

Redirect responses

See [Handler](/essential/handler.html#redirect)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', () => 'hi')
    .get('/redirect', ({ redirect }) => {
        return redirect('/')
    })
    .listen(3000)
```

## Plugin

Create a separate instance

See [Plugin](/essential/plugin)

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .state('plugin-version', 1)
    .get('/hi', () => 'hi')

new Elysia()
    .use(plugin)
    .get('/version', ({ store }) => store['plugin-version'])
    .listen(3000)
```

## WebSocket

Create a realtime connection using WebSocket

See [Web Socket](/patterns/websocket)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .ws('/ping', {
        message(ws, message) {
            ws.send('hello ' + message)
        }
    })
    .listen(3000)
```

## OpenAPI documentation

Create interactive documentation using Scalar (or optionally Swagger)

See [openapi](/plugins/openapi.html)

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'

const app = new Elysia()
    .use(openapi())
    .listen(3000)

console.log(`View documentation at "${app.server!.url}openapi" in your browser`);
```

## Unit Test

Write a unit test for your Elysia app

See [Unit Test](/patterns/unit-test)

```typescript
// test/index.test.ts
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'

describe('Elysia', () => {
    it('return a response', async () => {
        const app = new Elysia().get('/', () => 'hi')

        const response = await app
            .handle(new Request('http://localhost/'))
            .then((res) => res.text())

        expect(response).toBe('hi')
    })
})
```

## Custom body parser

Create custom logic for parsing bodies

See [Parse](/essential/life-cycle.html#parse)

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onParse(({ request, contentType }) => {
        if (contentType === 'application/custom-type')
            return request.text()
    })
```

## GraphQL

Create a custom GraphQL server using GraphQL Yoga or Apollo

See [GraphQL Yoga](/plugins/graphql-yoga)

```typescript
import { Elysia } from 'elysia'
import { yoga } from '@elysia/graphql-yoga'

const app = new Elysia()
    .use(
        yoga({
            typeDefs: /* GraphQL */`
                type Query {
                    hi: String
                }
            `,
            resolvers: {
                Query: {
                    hi: () => 'Hello from Elysia'
                }
            }
        })
    )
    .listen(3000)
```

---

---
url: 'https://elysiajs.com/patterns/configuration.md'
---

# Config

Elysia comes with a configurable behavior, allowing us to customize various aspects of its functionality.

We can define a configuration by using a constructor.

```ts
import { Elysia, t } from 'elysia'

new Elysia({
	prefix: '/v1',
	normalize: true
})
```

## adapter

###### Since 1.1.11

Runtime adapter for using Elysia in different environments.

Defaults to appropriate adapter based on the environment.

```ts
import { Elysia, t } from 'elysia'
import { BunAdapter } from 'elysia/adapter/bun'

new Elysia({
	adapter: BunAdapter
})
```

## allowUnsafeValidationDetails

###### Since 1.4.13

Whether Elysia should include unsafe validation details in the error response on production.

```ts
import { Elysia, t } from 'elysia'

new Elysia({
	allowUnsafeValidationDetails: true
})
```

By default, Elysia will omit all validation detail on production.

This is done to prevent leaking sensitive information about the validation schema, such as field names and expected types, which could be exploited by an attacker.

Ideally, this should only be enabled on public APIs as it may leak sensitive information about the server implementation.

#### Options - @default `false`

* `true` - Include unsafe validation details in the error response on production
* `false` - Exclude unsafe validation details in the error response on production

## aot

###### Since 0.4.0

Ahead of Time compilation.

Elysia has a built-in JIT *"compiler"* that can [optimize performance](/blog/elysia-04.html#ahead-of-time-complie).

```ts
import { Elysia } from 'elysia'

new Elysia({
	aot: true
})
```

Disable Ahead of Time compilation

#### Options - @default `false`

* `true` - Precompile every route before starting the server

* `false` - Disable JIT entirely. Faster startup time without cost of performance

## detail

Define an OpenAPI schema for all routes of an instance.

This schema will be used to generate OpenAPI documentation for all routes of an instance.

```ts
import { Elysia } from 'elysia'

new Elysia({
	detail: {
		hide: true,
		tags: ['elysia']
	}
})
```

## encodeSchema

Handle custom `t.Transform` schemas with custom `Encode` before returning the response to client.

This allows us to create custom encode functions for your data before sending response to the client.

```ts
import { Elysia, t } from 'elysia'

new Elysia({ encodeSchema: true })
```

#### Options - @default `true`

* `true` - Run `Encode` before sending the response to client
* `false` - Skip `Encode` entirely

## name

Define the name of an instance which is used for debugging and [Plugin Deduplication](/essential/plugin.html#plugin-deduplication)

```ts
import { Elysia } from 'elysia'

new Elysia({
	name: 'service.thing'
})
```

## nativeStaticResponse

###### Since 1.1.11

Use optimized functions for handling inline values for each respective runtime.

```ts
import { Elysia } from 'elysia'

new Elysia({
	nativeStaticResponse: true
})
```

#### Example

If enabled on Bun, Elysia will insert inline value into `Bun.serve.static` improving performance for static value.

```ts
import { Elysia } from 'elysia'

// This
new Elysia({
	nativeStaticResponse: true
}).get('/version', 1)

// is an equivalent to
Bun.serve({
	static: {
		'/version': new Response(1)
	}
})
```

## normalize

###### Since 1.1.0

Whether Elysia should coerce fields into a specified schema.

```ts
import { Elysia, t } from 'elysia'

new Elysia({
	normalize: true
})
```

When unknown properties that are not specified in schema are found on either input and output, how should Elysia handle the field?

Options - @default `true`

* `true`: Elysia will coerce fields into a specified schema using [exact mirror](/blog/elysia-13.html#exact-mirror)

* `typebox`: Elysia will coerce fields into a specified schema using [TypeBox's Value.Clean](https://github.com/sinclairzx81/typebox)

* `false`: Elysia will raise an error if a request or response contains fields that are not explicitly allowed in the schema of the respective handler.

## precompile

###### Since 1.0.0

Whether Elysia should [precompile all routes](/blog/elysia-10.html#improved-startup-time) ahead of time before starting the server.

```ts
import { Elysia } from 'elysia'

new Elysia({
	precompile: true
})
```

Options - @default `false`

* `true`: Run JIT on all routes before starting the server

* `false`: Dynamically compile routes on demand

It's recommended to leave it as `false`.

## prefix

Define a prefix for all routes of an instance

```ts
import { Elysia, t } from 'elysia'

new Elysia({
	prefix: '/v1'
})
```

When prefix is defined, all routes will be prefixed with the given value.

#### Example

```ts
import { Elysia, t } from 'elysia'

new Elysia({ prefix: '/v1' }).get('/name', 'elysia') // Path is /v1/name
```

## sanitize

A function or an array of functions that calls and intercepts on every `t.String` while validation.

Allowing us to read and transform strings into new values.

```ts
import { Elysia, t } from 'elysia'

new Elysia({
	sanitize: (value) => Bun.escapeHTML(value)
})
```

## seed

Define a value that will be used to generate checksum of an instance, used for [Plugin Deduplication](/essential/plugin.html#plugin-deduplication)

```ts
import { Elysia } from 'elysia'

new Elysia({
	seed: {
		value: 'service.thing'
	}
})
```

The value could be any type not limited to string, number, or object.

## strictPath

Whether Elysia should handle paths strictly.

According to [RFC 3986](https://tools.ietf.org/html/rfc3986#section-3.3), a path should be strictly equal to the path defined in the route.

```ts
import { Elysia, t } from 'elysia'

new Elysia({ strictPath: true })
```

#### Options - @default `false`

* `true` - Follows [RFC 3986](https://tools.ietf.org/html/rfc3986#section-3.3) for path matching strictly
* `false` - Tolerate suffix '/' or vice-versa.

#### Example

```ts
import { Elysia, t } from 'elysia'

// Path can be either /name or /name/
new Elysia({ strictPath: false }).get('/name', 'elysia')

// Path can be only /name
new Elysia({ strictPath: true }).get('/name', 'elysia')
```

## serve

Customize HTTP server behavior.

Bun serve configuration.

```ts
import { Elysia } from 'elysia'

new Elysia({
	serve: {
		hostname: 'elysiajs.com',
		tls: {
			cert: Bun.file('cert.pem'),
			key: Bun.file('key.pem')
		}
	},
})
```

This configuration extends [Bun Serve API](https://bun.sh/docs/api/http) and [Bun TLS](https://bun.sh/docs/api/http#tls)

### Example: Max body size

We can set the maximum body size by setting [`serve.maxRequestBodySize`](#serve-maxrequestbodysize) in the `serve` configuration.

```ts
import { Elysia } from 'elysia'

new Elysia({
	serve: {
		maxRequestBodySize: 1024 * 1024 * 256 // 256MB
	}
})
```

By default the maximum request body size is 128MB (1024 \* 1024 \* 128).
Define body size limit.

```ts
import { Elysia } from 'elysia'

new Elysia({
	serve: {
		// Maximum message size (in bytes)
	    maxPayloadLength: 64 * 1024,
	}
})
```

### Example: HTTPS / TLS

We can enable TLS (known as successor of SSL) by passing in a value for key and cert; both are required to enable TLS.

```ts
import { Elysia, file } from 'elysia'

new Elysia({
	serve: {
		tls: {
			cert: file('cert.pem'),
			key: file('key.pem')
		}
	}
})
```

### Example: Increase timeout

We can increase the idle timeout by setting [`serve.idleTimeout`](#serve-idletimeout) in the `serve` configuration.

```ts
import { Elysia } from 'elysia'

new Elysia({
	serve: {
		// Increase idle timeout to 60 seconds
		idleTimeout: 60
	}
})
```

By default the idle timeout is 30 seconds.

***

## serve

HTTP server configuration.

Elysia extends Bun configuration which supports TLS out of the box, powered by BoringSSL.

See [serve.tls](#serve-tls) for available configuration.

### serve.hostname

@default `0.0.0.0`

Set the hostname which the server listens on

### serve.id

Uniquely identify a server instance with an ID

This string will be used to hot reload the server without interrupting pending requests or websockets. If not provided, a value will be generated. To disable hot reloading, set this value to `null`.

### serve.idleTimeout

@default `30` (30 seconds)

By default, Elysia sets idle timeout to 30 seconds, which means that if a request is not completed within 30 seconds, it will be aborted.

### serve.maxRequestBodySize

@default `1024 * 1024 * 128` (128MB)

Set the maximum size of a request body (in bytes)

### serve.port

@default `3000`

Port to listen on

### serve.rejectUnauthorized

@default `NODE_TLS_REJECT_UNAUTHORIZED` environment variable

If set to `false`, any certificate is accepted.

### serve.reusePort

@default `true`

If the `SO_REUSEPORT` flag should be set

This allows multiple processes to bind to the same port, which is useful for load balancing

This configuration is overridden and turns on by default by Elysia

### serve.unix

If set, the HTTP server will listen on a unix socket instead of a port.

(Cannot be used with hostname+port)

### serve.tls

We can enable TLS (known as successor of SSL) by passing in a value for key and cert; both are required to enable TLS.

```ts
import { Elysia, file } from 'elysia'

new Elysia({
	serve: {
		tls: {
			cert: file('cert.pem'),
			key: file('key.pem')
		}
	}
})
```

Elysia extends Bun configuration which supports TLS out of the box, powered by BoringSSL.

### serve.tls.ca

Optionally override the trusted CA certificates. Default is to trust the well-known CAs curated by Mozilla.

Mozilla's CAs are completely replaced when CAs are explicitly specified using this option.

### serve.tls.cert

Cert chains in PEM format. One cert chain should be provided per private key.

Each cert chain should consist of the PEM formatted certificate for a provided private key, followed by the PEM formatted intermediate certificates (if any), in order, and not
including the root CA (the root CA must be pre-known to the peer, see ca).

When providing multiple cert chains, they do not have to be in the same order as their private keys in key.

If the intermediate certificates are not provided, the peer will not be
able to validate the certificate, and the handshake will fail.

### serve.tls.dhParamsFile

File path to a .pem file custom Diffie Helman parameters

### serve.tls.key

Private keys in PEM format. PEM allows the option of private keys being encrypted. Encrypted keys will be decrypted with options.passphrase.

Multiple keys using different algorithms can be provided either as an array of unencrypted key strings or buffers, or an array of objects in the form .

The object form can only occur in an array.

**object.passphrase** is optional. Encrypted keys will be decrypted with

**object.passphrase** if provided, or **options.passphrase** if it is not.

### serve.tls.lowMemoryMode

@default `false`

This sets `OPENSSL_RELEASE_BUFFERS` to 1.

It reduces overall performance but saves some memory.

### serve.tls.passphrase

Shared passphrase for a single private key and/or a PFX.

### serve.tls.requestCert

@default `false`

If set to `true`, the server will request a client certificate.

### serve.tls.secureOptions

Optionally affect the OpenSSL protocol behavior, which is not usually necessary.

This should be used carefully if at all!

Value is a numeric bitmask of the SSL\_OP\_\* options from OpenSSL Options

### serve.tls.serverName

Explicitly set a server name

## tags

Define tags for OpenAPI schema for all routes of an instance similar to [detail](#detail)

```ts
import { Elysia } from 'elysia'

new Elysia({
	tags: ['elysia']
})
```

## systemRouter

Use runtime/framework provided router if possible.

On Bun, Elysia will use [Bun.serve.routes](https://bun.sh/docs/api/http#routing) and fallback to Elysia's own router.

## websocket

Override websocket configuration

Recommended to leave this as default as Elysia will generate suitable configuration for handling WebSocket automatically

This configuration extends [Bun's WebSocket API](https://bun.sh/docs/api/websockets)

#### Example

```ts
import { Elysia } from 'elysia'

new Elysia({
	websocket: {
		// enable compression and decompression
    	perMessageDeflate: true
	}
})
```

***

---

---
url: 'https://elysiajs.com/tutorial/patterns/cookie.md'
---

# Cookie

You interact with cookies by using cookie from context.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ cookie: { visit } }) => {
		const total = +visit.value ?? 0
		visit.value++

		return `You have visited ${visit.value} times`
	})
	.listen(3000)
```

Cookie is a reactive object. Once modified, it will be reflected in response.

## Value

Elysia will then try to coerce it into its respective value when a type annotation if provided.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ cookie: { visit } }) => {
		visit.value ??= 0
		visit.value.total++

		return `You have visited ${visit.value.total} times`
	}, {
		cookie: t.Object({
			visit: t.Optional(
				t.Object({
					total: t.Number()
				})
			)
		})
	})
	.listen(3000)
```

We can use cookie schema to validate and parse cookie.

## Attribute

We can get/set cookie attribute by its respective property name.

Otherwise, use `.set()` to bulk set attribute.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ cookie: { visit } }) => {
		visit.value ??= 0
		visit.value++

		visit.httpOnly = true
		visit.path = '/'

		visit.set({
			sameSite: 'lax',
			secure: true,
			maxAge: 60 * 60 * 24 * 7
		})

		return `You have visited ${visit.value} times`
	})
	.listen(3000)
```

See Cookie Attribute.

## Remove

We can remove cookie by calling `.remove()` method.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ cookie: { visit } }) => {
		visit.remove()

		return `Cookie removed`
	})
	.listen(3000)
```

## Cookie Signature

Elysia can sign cookies to prevent tampering by:

1. Provide a cookie secret to the Elysia constructor.
2. Use `t.Cookie` to provide secret for each cookie.

```typescript
import { Elysia } from 'elysia'

new Elysia({
	cookie: {
		secret: 'Fischl von Luftschloss Narfidort',
	}
})
	.get('/', ({ cookie: { visit } }) => {
		visit.value ??= 0
		visit.value++

		return `You have visited ${visit.value} times`
	}, {
		cookie: t.Cookie({
			visit: t.Optional(t.Number())
        }, {
            secrets: 'Fischl von Luftschloss Narfidort',
            sign: ['visit']
        })
	})
	.listen(3000)
```

If multiple secrets are provided, Elysia will use the first secret to sign cookies, and try to verify with the rest.

See Cookie Signature, Cookie Rotation.

## Assignment

Let's create a simple counter that tracks how many times you have visited the site.

\<template #answer>

1. We can update the cookie value by modifying `visit.value`.
2. We can set **HTTP only** attribute by setting `visit.httpOnly = true`.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/', ({ cookie: { visit } }) => {
		visit.value ??= 0
		visit.value++

		visit.httpOnly = true

		return `You have visited ${visit.value} times`
	}, {
		cookie: t.Object({
			visit: t.Optional(
				t.Number()
			)
		})
	})
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/plugins/cors.md'
---

# CORS Plugin

This plugin adds support for customizing [Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) behavior.

Install with:

```bash
bun add @elysia/cors
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { cors } from '@elysia/cors'

new Elysia().use(cors()).listen(3000)
```

This will set Elysia to accept requests from any origin.

## Config

Below is the config that is accepted by the plugin

### origin

@default `true`

Indicates whether the response can be shared with the requesting code from the given origins.

Value can be one of the following:

* **string** - Name of origin which will directly assign to [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) header.
* **boolean** - If set to true, [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) will be set to `*` (any origins)
* **RegExp** - Pattern to match request's URL, allowed if matched.
* **Function** - Custom logic to allow resource sharing, allow if `true` is returned.
  * Expected to have the type of:
  ```typescript
  cors(context: Context) => boolean | void
  ```
* **Array\<string | RegExp | Function>** - iterate through all cases above in order, allowed if any of the values are `true`.

***

### methods

@default `*`

Allowed methods for cross-origin requests.

Assign [Access-Control-Allow-Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods) header.

Value can be one of the following:

* **undefined | null | ''** - Ignore all methods.
* **\*** - Allows all methods.
* **string** - Expects either a single method or a comma-delimited string
  * (eg: `'GET, PUT, POST'`)
* **string\[]** - Allow multiple HTTP methods.
  * eg: `['GET', 'PUT', 'POST']`

***

### allowedHeaders

@default `*`

Allowed headers for an incoming request.

Assign [Access-Control-Allow-Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers) header.

Value can be one of the following:

* **string** - Expects either a single header or a comma-delimited string
  * eg: `'Content-Type, Authorization'`.
* **string\[]** - Allow multiple HTTP headers.
  * eg: `['Content-Type', 'Authorization']`

***

### exposeHeaders

@default `*`

Response CORS with specified headers.

Assign [Access-Control-Expose-Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers) header.

Value can be one of the following:

* **string** - Expects either a single header or a comma-delimited string.
  * eg: `'Content-Type, X-Powered-By'`.
* **string\[]** - Allow multiple HTTP headers.
  * eg: `['Content-Type', 'X-Powered-By']`

***

### credentials

@default `true`

The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to the frontend JavaScript code when the request's credentials mode [Request.credentials](https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials) is `include`.

When a request's credentials mode [Request.credentials](https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials) is `include`, browsers will only expose the response to the frontend JavaScript code if the Access-Control-Allow-Credentials value is true.

Credentials are cookies, authorization headers, or TLS client certificates.

Assign [Access-Control-Allow-Credentials](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials) header.

***

### maxAge

@default `5`

Indicates how long the results of a [preflight request](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request) (that is the information contained in the [Access-Control-Allow-Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods) and [Access-Control-Allow-Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers) headers) can be cached.

Assign [Access-Control-Max-Age](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age) header.

***

### preflight

The preflight request is a request sent to check if the CORS protocol is understood and if a server is aware of using specific methods and headers.

Response with **OPTIONS** request with 3 HTTP request headers:

* **Access-Control-Request-Method**
* **Access-Control-Request-Headers**
* **Origin**

This config indicates if the server should respond to preflight requests.

## Pattern

Below you can find the common patterns to use the plugin.

## Allow CORS by top-level domain

```typescript
import { Elysia } from 'elysia'
import { cors } from '@elysia/cors'

const app = new Elysia()
	.use(
		cors({
			origin: /.*\.saltyaom\.com$/
		})
	)
	.get('/', () => 'Hi')
	.listen(3000)
```

This will allow requests from top-level domains with `saltyaom.com`

---

---
url: 'https://elysiajs.com/plugins/cron.md'
---

# Cron Plugin

This plugin adds support for running cron jobs in the Elysia server.

Install with:

```bash
bun add @elysia/cron
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { cron } from '@elysia/cron'

new Elysia()
	.use(
		cron({
			name: 'heartbeat',
			pattern: '*/10 * * * * *',
			run() {
				console.log('Heartbeat')
			}
		})
	)
	.listen(3000)
```

The above code will log `heartbeat` every 10 seconds.

## cron

Create a cron job for the Elysia server.

type:

```
cron(config: CronConfig, callback: (Instance['store']) => void): this
```

`CronConfig` accepts the parameters specified below:

### name

Job name to register to `store`.

This will register the cron instance to `store` with a specified name, which can be referenced in later processes, e.g., to stop the job.

### pattern

Time to run the job as specified by [cron syntax](https://en.wikipedia.org/wiki/Cron) specified as below:

```
┌────────────── second (optional)
│ ┌──────────── minute
│ │ ┌────────── hour
│ │ │ ┌──────── day of the month
│ │ │ │ ┌────── month
│ │ │ │ │ ┌──── day of week
│ │ │ │ │ │
* * * * * *
```

This can be generated by tools like [Crontab Guru](https://crontab.guru/)

***

This plugin extends the cron method to Elysia using [cronner](https://github.com/hexagon/croner).

Below is the config accepted by cronner.

### timezone

Time zone in Europe/Stockholm format

### startAt

Schedule start time for the job

### stopAt

Schedule stop time for the job

### maxRuns

Maximum number of executions

### catch

Continue execution even if an unhandled error is thrown by a triggered function.

### interval

The minimum interval between executions, in seconds.

## Pattern

Below you can find the common patterns to use the plugin.

## Stop cron job

You can stop the cron job manually by accessing the cron job name registered to `store`.

```typescript
import { Elysia } from 'elysia'
import { cron } from '@elysia/cron'

const app = new Elysia()
	.use(
		cron({
			name: 'heartbeat',
			pattern: '*/1 * * * * *',
			run() {
				console.log('Heartbeat')
			}
		})
	)
	.get(
		'/stop',
		({
			store: {
				cron: { heartbeat }
			}
		}) => {
			heartbeat.stop()

			return 'Stop heartbeat'
		}
	)
	.listen(3000)
```

## Predefined patterns

You can use predefined patterns from `@elysia/cron/schedule`

```typescript
import { Elysia } from 'elysia'
import { cron, Patterns } from '@elysia/cron'

const app = new Elysia()
	.use(
		cron({
			name: 'heartbeat',
			pattern: Patterns.everySecond(),
			run() {
				console.log('Heartbeat')
			}
		})
	)
	.get(
		'/stop',
		({
			store: {
				cron: { heartbeat }
			}
		}) => {
			heartbeat.stop()

			return 'Stop heartbeat'
		}
	)
	.listen(3000)
```

### Functions

| Function                                 | Description                                           |
| ---------------------------------------- | ----------------------------------------------------- |
| `.everySeconds(2)`                       | Run the task every 2 seconds                          |
| `.everyMinutes(5)`                       | Run the task every 5 minutes                          |
| `.everyHours(3)`                         | Run the task every 3 hours                            |
| `.everyHoursAt(3, 15)`                   | Run the task every 3 hours at 15 minutes              |
| `.everyDayAt('04:19')`                   | Run the task every day at 04:19                       |
| `.everyWeekOn(Patterns.MONDAY, '19:30')` | Run the task every Monday at 19:30                    |
| `.everyWeekdayAt('17:00')`               | Run the task every day from Monday to Friday at 17:00 |
| `.everyWeekendAt('11:00')`               | Run the task on Saturday and Sunday at 11:00          |

### Function aliases to constants

| Function          | Constant                           |
| ----------------- | ---------------------------------- |
| `.everySecond()`  | EVERY\_SECOND                       |
| `.everyMinute()`  | EVERY\_MINUTE                       |
| `.hourly()`       | EVERY\_HOUR                         |
| `.daily()`        | EVERY\_DAY\_AT\_MIDNIGHT              |
| `.everyWeekday()` | EVERY\_WEEKDAY                      |
| `.everyWeekend()` | EVERY\_WEEKEND                      |
| `.weekly()`       | EVERY\_WEEK                         |
| `.monthly()`      | EVERY\_1ST\_DAY\_OF\_MONTH\_AT\_MIDNIGHT |
| `.everyQuarter()` | EVERY\_QUARTER                      |
| `.yearly()`       | EVERY\_YEAR                         |

### Constants

| Constant                                 | Pattern              |
| ---------------------------------------- | -------------------- |
| `.EVERY_SECOND`                          | `* * * * * *`        |
| `.EVERY_5_SECONDS`                       | `*/5 * * * * *`      |
| `.EVERY_10_SECONDS`                      | `*/10 * * * * *`     |
| `.EVERY_30_SECONDS`                      | `*/30 * * * * *`     |
| `.EVERY_MINUTE`                          | `*/1 * * * *`        |
| `.EVERY_5_MINUTES`                       | `0 */5 * * * *`      |
| `.EVERY_10_MINUTES`                      | `0 */10 * * * *`     |
| `.EVERY_30_MINUTES`                      | `0 */30 * * * *`     |
| `.EVERY_HOUR`                            | `0 0-23/1 * * *`     |
| `.EVERY_2_HOURS`                         | `0 0-23/2 * * *`     |
| `.EVERY_3_HOURS`                         | `0 0-23/3 * * *`     |
| `.EVERY_4_HOURS`                         | `0 0-23/4 * * *`     |
| `.EVERY_5_HOURS`                         | `0 0-23/5 * * *`     |
| `.EVERY_6_HOURS`                         | `0 0-23/6 * * *`     |
| `.EVERY_7_HOURS`                         | `0 0-23/7 * * *`     |
| `.EVERY_8_HOURS`                         | `0 0-23/8 * * *`     |
| `.EVERY_9_HOURS`                         | `0 0-23/9 * * *`     |
| `.EVERY_10_HOURS`                        | `0 0-23/10 * * *`    |
| `.EVERY_11_HOURS`                        | `0 0-23/11 * * *`    |
| `.EVERY_12_HOURS`                        | `0 0-23/12 * * *`    |
| `.EVERY_DAY_AT_1AM`                      | `0 01 * * *`         |
| `.EVERY_DAY_AT_2AM`                      | `0 02 * * *`         |
| `.EVERY_DAY_AT_3AM`                      | `0 03 * * *`         |
| `.EVERY_DAY_AT_4AM`                      | `0 04 * * *`         |
| `.EVERY_DAY_AT_5AM`                      | `0 05 * * *`         |
| `.EVERY_DAY_AT_6AM`                      | `0 06 * * *`         |
| `.EVERY_DAY_AT_7AM`                      | `0 07 * * *`         |
| `.EVERY_DAY_AT_8AM`                      | `0 08 * * *`         |
| `.EVERY_DAY_AT_9AM`                      | `0 09 * * *`         |
| `.EVERY_DAY_AT_10AM`                     | `0 10 * * *`         |
| `.EVERY_DAY_AT_11AM`                     | `0 11 * * *`         |
| `.EVERY_DAY_AT_NOON`                     | `0 12 * * *`         |
| `.EVERY_DAY_AT_1PM`                      | `0 13 * * *`         |
| `.EVERY_DAY_AT_2PM`                      | `0 14 * * *`         |
| `.EVERY_DAY_AT_3PM`                      | `0 15 * * *`         |
| `.EVERY_DAY_AT_4PM`                      | `0 16 * * *`         |
| `.EVERY_DAY_AT_5PM`                      | `0 17 * * *`         |
| `.EVERY_DAY_AT_6PM`                      | `0 18 * * *`         |
| `.EVERY_DAY_AT_7PM`                      | `0 19 * * *`         |
| `.EVERY_DAY_AT_8PM`                      | `0 20 * * *`         |
| `.EVERY_DAY_AT_9PM`                      | `0 21 * * *`         |
| `.EVERY_DAY_AT_10PM`                     | `0 22 * * *`         |
| `.EVERY_DAY_AT_11PM`                     | `0 23 * * *`         |
| `.EVERY_DAY_AT_MIDNIGHT`                 | `0 0 * * *`          |
| `.EVERY_WEEK`                            | `0 0 * * 0`          |
| `.EVERY_WEEKDAY`                         | `0 0 * * 1-5`        |
| `.EVERY_WEEKEND`                         | `0 0 * * 6,0`        |
| `.EVERY_1ST_DAY_OF_MONTH_AT_MIDNIGHT`    | `0 0 1 * *`          |
| `.EVERY_1ST_DAY_OF_MONTH_AT_NOON`        | `0 12 1 * *`         |
| `.EVERY_2ND_HOUR`                        | `0 */2 * * *`        |
| `.EVERY_2ND_HOUR_FROM_1AM_THROUGH_11PM`  | `0 1-23/2 * * *`     |
| `.EVERY_2ND_MONTH`                       | `0 0 1 */2 *`        |
| `.EVERY_QUARTER`                         | `0 0 1 */3 *`        |
| `.EVERY_6_MONTHS`                        | `0 0 1 */6 *`        |
| `.EVERY_YEAR`                            | `0 0 1 1 *`          |
| `.EVERY_30_MINUTES_BETWEEN_9AM_AND_5PM`  | `0 */30 9-17 * * *`  |
| `.EVERY_30_MINUTES_BETWEEN_9AM_AND_6PM`  | `0 */30 9-18 * * *`  |
| `.EVERY_30_MINUTES_BETWEEN_10AM_AND_7PM` | `0 */30 10-19 * * *` |

---

---
url: 'https://elysiajs.com/integrations/vercel.md'
---

# Deploy Elysia on Vercel

Elysia can be deployed on Vercel with zero configuration using either Bun or Node runtime.

1. In **src/index.ts**, create or import an existing Elysia server
2. Export the Elysia server as default export

```typescript
import { Elysia, t } from 'elysia'

export default new Elysia() // [!code ++]
    .get('/', () => 'Hello Vercel Function')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })
```

3. Develop locally with Vercel CLI

```bash
vc dev
```

4. Deploy to Vercel

```bash
vc deploy
```

That's it. Your Elysia app is now running on Vercel.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

### Using Node.js

To deploy with Node.js, make sure to set `type: module` in your `package.json`

::: code-group

```ts [package.json]
{
  "name": "elysia-app",
  "type": "module" // [!code ++]
}
```

:::

### Using Bun

To deploy with Bun, make sure to set the runtime to Bun in your `vercel.json`

::: code-group

```ts [vercel.json]
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "bunVersion": "1.x" // [!code ++]
}
```

## If this doesn't work

Vercel has zero-configuration support for Elysia. For additional configuration, please refer to the [Vercel documentation](https://vercel.com/docs/frameworks/backend/elysia)

---

---
url: 'https://elysiajs.com/patterns/deploy.md'
---

# Deploy to production

This page provides a guide on how to deploy Elysia to production.

## Cluster mode

Elysia is single-threaded by default. To take advantage of multi-core CPU, we can run Elysia in cluster mode.

Let's create an **index.ts** file that imports our main server from **server.ts** and fork multiple workers based on the number of CPU cores available.

::: code-group

```ts [src/index.ts]
import cluster from 'node:cluster'
import os from 'node:os'
import process from 'node:process'

if (cluster.isPrimary) {
  	for (let i = 0; i < os.availableParallelism(); i++)
    	cluster.fork()
} else {
  	await import('./server')
  	console.log(`Worker ${process.pid} started`)
}
```

```ts [src/server.ts]
import { Elysia } from 'elysia'

new Elysia()
	.get('/', () => 'Hello World!')
	.listen(3000)
```

:::

This will ensure that Elysia is running on multiple CPU cores.

::: tip
Elysia on Bun uses SO\_REUSEPORT by default, which allows multiple instances to listen on the same port. This only works on Linux.
:::

## Compile to binary

We recommend running the build command before deploying to production as it could potentially reduce memory usage and file size significantly.

We recommend compiling Elysia into a single binary using the command as follows:

```bash
bun build \
	--compile \
	--minify-whitespace \
	--minify-syntax \
	--target bun \
	--outfile server \
	src/index.ts
```

This will generate a portable binary `server` which we can run to start our server.

Compiling server to binary usually significantly reduces memory usage by 2-3x compared to development environment.

This command is a bit long, so let's break it down:

1. **--compile** Compile TypeScript to binary
2. **--minify-whitespace** Remove unnecessary whitespace
3. **--minify-syntax** Minify JavaScript syntax to reduce file size
4. **--target bun** Optimize the binary for Bun runtime
5. **--outfile server** Output the binary as `server`
6. **src/index.ts** The entry file of our server (codebase)

To start our server, simply run the binary.

```bash
./server
```

Once binary is compiled, you don't need `Bun` installed on the machine to run the server.

This is great as the deployment server doesn't need to install an extra runtime to run making binary portable.

### Target

You can also add a `--target` flag to optimize the binary for the target platform.

```bash
bun build \
	--compile \
	--minify-whitespace \
	--minify-syntax \
	--target bun-linux-x64 \
	--outfile server \
	src/index.ts
```

Here's a list of available targets:
| Target                  | Operating System | Architecture | Modern | Baseline | Libc  |
|--------------------------|------------------|--------------|--------|----------|-------|
| bun-linux-x64           | Linux            | x64          | ✅      | ✅        | glibc |
| bun-linux-arm64         | Linux            | arm64        | ✅      | N/A      | glibc |
| bun-windows-x64         | Windows          | x64          | ✅      | ✅        | -     |
| bun-windows-arm64       | Windows          | arm64        | ❌      | ❌        | -     |
| bun-darwin-x64          | macOS            | x64          | ✅      | ✅        | -     |
| bun-darwin-arm64        | macOS            | arm64        | ✅      | N/A      | -     |
| bun-linux-x64-musl      | Linux            | x64          | ✅      | ✅        | musl  |
| bun-linux-arm64-musl    | Linux            | arm64        | ✅      | N/A      | musl  |

### Why not --minify

Bun has a `--minify` flag that will minify the binary.

However if we are using [OpenTelemetry](/plugins/opentelemetry), it will reduce a function name to a single character.

This makes tracing harder than it should as OpenTelemetry relies on function names.

However, if you're not using OpenTelemetry, you may opt in for `--minify` instead

```bash
bun build \
	--compile \
	--minify \
	--outfile server \
	src/index.ts
```

### Permission

Some Linux distributions might not be able to run the binary, we suggest enabling execute permissions on the binary if you're on Linux:

```bash
chmod +x ./server

./server
```

### Unknown random Chinese error

If you're trying to deploy a binary to your server but are unable to run it and are receiving random Chinese character errors.

It means that the machine you're running on **doesn't support AVX2**.

Unfortunately, Bun requires a machine that has `AVX2` hardware support.

There's no known workaround.

## Compile to JavaScript

If you are unable to compile to a binary or you are deploying on a Windows server.

You may bundle your server to a JavaScript file instead.

```bash
bun build \
	--minify-whitespace \
	--minify-syntax \
	--outfile ./dist/index.js \
	src/index.ts
```

This will generate a single portable JavaScript file that you can deploy on your server.

```bash
NODE_ENV=production bun ./dist/index.js
```

## Docker

On Docker, we recommend always compiling to a binary to reduce base image overhead.

Here's an example image using the Distroless image with a binary.

```dockerfile [Dockerfile]
FROM oven/bun AS build

WORKDIR /app

# Cache packages installation
COPY package.json package.json
COPY bun.lock bun.lock

RUN bun install

COPY ./src ./src

ENV NODE_ENV=production

RUN bun build \
	--compile \
	--minify-whitespace \
	--minify-syntax \
	--outfile server \
	src/index.ts

FROM gcr.io/distroless/base

WORKDIR /app

COPY --from=build /app/server server

ENV NODE_ENV=production

CMD ["./server"]

EXPOSE 3000
```

### OpenTelemetry

If you are using [OpenTelemetry](/patterns/opentelemetry) to deploy production server.

As OpenTelemetry relies on monkey-patching `node_modules/<library>`. It's required to make instrumentations work properly, we need to specify libraries to be instrumented as an external module to exclude it from being bundled.

For example, if you are using `@opentelemetry/instrumentation-pg` to instrument the `pg` library. We need to exclude `pg` from being bundled and make sure that it is importing `node_modules/pg`.

To make this work, we may specify `pg` as an external module with `--external pg`

```bash
bun build --compile --external pg --outfile server src/index.ts
```

This tells bun not to bundle `pg` into the final output file, and will be imported from the `node_modules` directory at runtime. So on a production server, you must also keep the `node_modules` directory.

It's recommended to specify packages that should be available in a production server as `dependencies` in `package.json` and use `bun install --production` to install only production dependencies.

```json
{
	"dependencies": {
		"pg": "^8.15.6"
	},
	"devDependencies": {
		"@elysia/opentelemetry": "^1.2.0",
		"@opentelemetry/instrumentation-pg": "^0.52.0",
		"@types/pg": "^8.11.14",
		"elysia": "^1.2.25"
	}
}
```

Then after running a build command, on a production server

```bash
bun install --production
```

If the node\_modules directory still includes development dependencies, you may remove the node\_modules directory and reinstall production dependencies again.

### Monorepo

If you are using Elysia with Monorepo, you may need to include dependent `packages`.

If you are using Turborepo, you may place a Dockerfile inside your apps directory like **apps/server/Dockerfile**. This also applies to other monorepo managers such as Lerna, etc.

Assuming that our monorepo uses Turborepo with structure as follows:

* apps
  * server
    * **Dockerfile (place a Dockerfile here)**
* packages
  * config

Then we can build our Dockerfile on monorepo root (not app root):

```bash
docker build -f apps/server/Dockerfile -t elysia-mono .
```

With Dockerfile as follows:

```dockerfile [apps/server/Dockerfile]
FROM oven/bun:1 AS build

WORKDIR /app

# Cache packages
COPY package.json package.json
COPY bun.lock bun.lock

COPY /apps/server/package.json ./apps/server/package.json
COPY /packages/config/package.json ./packages/config/package.json

RUN bun install

COPY /apps/server ./apps/server
COPY /packages/config ./packages/config

ENV NODE_ENV=production

RUN bun build \
	--compile \
	--minify-whitespace \
	--minify-syntax \
	--outfile server \
	src/index.ts

FROM gcr.io/distroless/base

WORKDIR /app

COPY --from=build /app/server server

ENV NODE_ENV=production

CMD ["./server"]

EXPOSE 3000
```

## Railway

[Railway](https://railway.app) is one of the popular deployment platforms.

Railway assigns a **random port** to expose for each deployment, which can be accessed via the `PORT` environment variable.

We need to modify our Elysia server to accept the `PORT` environment variable to comply with Railway port.

Instead of a fixed port, we may use `process.env.PORT` and provide a fallback on development instead.

```ts
new Elysia()
	.listen(3000) // [!code --]
	.listen(process.env.PORT ?? 3000) // [!code ++]
```

This should allow Elysia to intercept port provided by Railway.

::: tip
Elysia assigns the hostname to `0.0.0.0` automatically, which works with Railway
:::

---

---
url: 'https://elysiajs.com/eden/fetch.md'
---

# Eden Fetch

A fetch-like alternative to Eden Treaty.

With Eden Fetch, you can interact with Elysia server in a type-safe manner using Fetch API.

***

First export your existing Elysia server type:

```typescript
// server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/hi', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app
```

Then import the server type, and consume the Elysia API on client:

```typescript
import { edenFetch } from '@elysia/eden'
import type { App } from './server'

const fetch = edenFetch<App>('http://localhost:3000')

// response type: 'Hi Elysia'
const pong = await fetch('/hi', {})

// response type: 1895
const id = await fetch('/id/:id', {
    params: {
        id: '1895'
    }
})

// response type: { id: 1895, name: 'Skadi' }
const nendoroid = await fetch('/mirror', {
    method: 'POST',
    body: {
        id: 1895,
        name: 'Skadi'
    }
})
```

## Error Handling

You can handle errors the same way as Eden Treaty:

```typescript
import { edenFetch } from '@elysia/eden'
import type { App } from './server'

const fetch = edenFetch<App>('http://localhost:3000')

// response type: { id: 1895, name: 'Skadi' }
const { data: nendoroid, error } = await fetch('/mirror', {
    method: 'POST',
    body: {
        id: 1895,
        name: 'Skadi'
    }
})

if(error) {
    switch(error.status) {
        case 400:
        case 401:
            throw error.value
            break

        case 500:
        case 502:
            throw error.value
            break

        default:
            throw error.value
            break
    }
}

const { id, name } = nendoroid
```

## When should I use Eden Fetch over Eden Treaty

Unlike Elysia < 1.0, Eden Fetch is not faster than Eden Treaty anymore.

The preference is based on you and your team's agreement; however, we recommend using [Eden Treaty](/eden/treaty/overview) instead.

For Elysia < 1.0:

Using Eden Treaty required a lot of down-level iteration to map all possible types in a single go, while in contrast, Eden Fetch could be lazily executed until you pick a route.

With complex types and many server routes, using Eden Treaty on a low-end development device could lead to slow type inference and auto-completion.

But as Elysia has tweaked and optimized a lot of types and inference, Eden Treaty can perform very well in the considerable amount of routes.

If your single process contains **more than 500 routes**, and you need to consume all of the routes **in a single frontend codebase**, then you might want to use Eden Fetch as it has a significantly better TypeScript performance than Eden Treaty.

---

---
url: 'https://elysiajs.com/eden/installation.md'
---

# Eden Installation

Start by installing Eden on your frontend:

```bash
bun add @elysia/eden
bun add -d elysia
```

::: tip
Eden needs Elysia to infer utility types.

Make sure to install Elysia with the version matching the server.
:::

First, export your existing Elysia server type:

```typescript
// server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]
```

Then consume the Elysia API on client side:

```typescript twoslash
// @filename: server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/', 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]

// @filename: index.ts
// ---cut---
// client.ts
import { treaty } from '@elysia/eden'
import type { App } from './server' // [!code ++]

const client = treaty<App>('localhost:3000') // [!code ++]

// response: Hi Elysia
const { data: index } = await client.get()

// response: 1895
const { data: id } = await client.id({ id: 1895 }).get()

// response: { id: 1895, name: 'Skadi' }
const { data: nendoroid } = await client.mirror.post({
    id: 1895,
    name: 'Skadi'
})

// @noErrors
client.
//     ^|
```

## Gotcha

Sometimes, Eden may not infer types from Elysia correctly. The following are the most common workarounds to fix Eden type inference.

### Type Strict

Make sure to enable strict mode in **tsconfig.json**

```json
{
  "compilerOptions": {
    "strict": true // [!code ++]
  }
}
```

### Mismatched Elysia version

Eden depends on the Elysia class to import the Elysia instance and infer types correctly.

Make sure that both the client and server have matching Elysia versions.

You can check it with [`npm why`](https://docs.npmjs.com/cli/v10/commands/npm-explain) command:

```bash
npm why elysia
```

The output should contain only one elysia version at the top level:

```
elysia@1.1.12
node_modules/elysia
  elysia@"1.1.25" from the root project
  peer elysia@">= 1.1.0" from @elysia/html@1.1.0
  node_modules/@elysia/html
    dev @elysia/html@"1.1.1" from the root project
  peer elysia@">= 1.1.0" from @elysia/opentelemetry@1.1.2
  node_modules/@elysia/opentelemetry
    dev @elysia/opentelemetry@"1.1.7" from the root project
  peer elysia@">= 1.1.0" from @elysia/swagger@1.1.0
  node_modules/@elysia/swagger
    dev @elysia/swagger@"1.1.6" from the root project
  peer elysia@">= 1.1.0" from @elysia/eden@1.1.2
  node_modules/@elysia/eden
    dev @elysia/eden@"1.1.3" from the root project
```

### TypeScript version

Elysia uses newer features and syntax of TypeScript to infer types in the most performant way. Features like Const Generics and Template Literals are heavily used.

Make sure your client has a **minimum TypeScript version of >= 5.0**

### Method Chaining

To make Eden work, Elysia must use **method chaining**

Elysia's type system is complex, methods usually introduce a new type to the instance.

Using method chaining will help save that new type reference.

For example:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .state('build', 1)
    // Store is strictly typed // [!code ++]
    .get('/', ({ store: { build } }) => build)
    .listen(3000)
```

Using this, **state** now returns a new **ElysiaInstance** type, introducing **build** into store replacing the current one.

Without method chaining, Elysia doesn't save the new type when introduced, leading to no type inference.

```typescript twoslash
// @errors: 2339
import { Elysia } from 'elysia'

const app = new Elysia()

app.state('build', 1)

app.get('/', ({ store: { build } }) => build)

app.listen(3000)
```

### Type Definitions

If you are using a Bun specific feature, like `Bun.file` or similar API and return it from a handler, you may need to install Bun type definitions to the client as well.

```bash
bun add -d @types/bun
```

### Path alias (monorepo)

If you are using path aliases in your monorepo, make sure that the frontend is able to resolve the path the same way as the backend.

::: tip
Setting up path aliases in a monorepo can be tricky. You can fork our example template: [Kozeki Template](https://github.com/SaltyAom/kozeki-template) and modify it to your needs.
:::

For example, if you have the following path alias for your backend in **tsconfig.json**:

```json
{
  "compilerOptions": {
  	"baseUrl": ".",
	"paths": {
	  "@/*": ["./src/*"]
	}
  }
}
```

And your backend code is like this:

```typescript
import { Elysia } from 'elysia'
import { a, b } from '@/controllers'

const app = new Elysia()
	.use(a)
	.use(b)
	.listen(3000)

export type app = typeof app
```

You **must** make sure that your frontend code is able to resolve the same path alias. Otherwise, type inference will be resolved as any.

```typescript
import { treaty } from '@elysia/eden'
import type { app } from '@/index'

const client = treaty<app>('localhost:3000')

// This should be able to resolve the same module in both frontend and backend, and not `any`
import { a, b } from '@/controllers' // [!code ++]
```

To fix this, you must make sure that the path alias is resolved to the same file in both the frontend and backend.

So, you must change the path alias in **tsconfig.json** to:

```json
{
  "compilerOptions": {
  	"baseUrl": ".",
	"paths": {
	  "@/*": ["../apps/backend/src/*"]
	}
  }
}
```

If configured correctly, you should be able to resolve the same module in both the frontend and backend.

```typescript
// This should be able to resolve the same module in both frontend and backend, and not `any`
import { a, b } from '@/controllers'
```

#### Namespace

We recommend adding a **namespace** prefix for each module in your monorepo to avoid any confusion and conflicts that may occur.

```json
{
  "compilerOptions": {
  	"baseUrl": ".",
	"paths": {
	  "@frontend/*": ["./apps/frontend/src/*"],
	  "@backend/*": ["./apps/backend/src/*"]
	}
  }
}
```

Then, you can import the module like this:

```typescript
// Should work in both frontend and backend and not return `any`
import { a, b } from '@backend/controllers'
```

We recommend creating a **single tsconfig.json** that defines a `baseUrl` as the root of your repo, provides a path according to the module location, and creates a **tsconfig.json** for each module that inherits the root **tsconfig.json** which has the path alias.

You may find a working example in this [path alias example repo](https://github.com/SaltyAom/elysia-monorepo-path-alias) or [Kozeki Template](https://github.com/SaltyAom/kozeki-template).

---

---
url: 'https://elysiajs.com/eden/test.md'
---

# Eden Test

Using Eden, we can create integration tests with end-to-end type safety and auto-completion.

## Setup

We can use [Bun test](https://bun.sh/guides/test/watch-mode) to create tests.

Create **test/index.test.ts** in the root of the project directory with the following:

```typescript
// test/index.test.ts
import { describe, expect, it } from 'bun:test'

import { edenTreaty } from '@elysia/eden'

const app = new Elysia()
    .get('/', () => 'hi')
    .listen(3000)

const api = edenTreaty<typeof app>('http://localhost:3000')

describe('Elysia', () => {
    it('return a response', async () => {
        const { data } = await api.get()

        expect(data).toBe('hi')
    })
})
```

Then we can perform tests by running **bun test**

```bash
bun test
```

This allows us to perform integration tests programmatically instead of manual fetch, while supporting type checking automatically.

---

---
url: 'https://elysiajs.com/eden/treaty/config.md'
---

# Config

Eden Treaty accepts 2 parameters:

* **urlOrInstance** - URL endpoint or Elysia instance
* **options** (optional) - Customize fetch behavior

## urlOrInstance

Accepts either a URL endpoint as a string or a literal Elysia instance.

Eden will change the behavior based on the type as follows:

### URL Endpoint (string)

If a URL endpoint is passed, Eden Treaty will use `fetch` or `config.fetcher` to create a network request to an Elysia instance.

```typescript
import { treaty } from '@elysia/eden'
import type { App } from './server'

const api = treaty<App>('localhost:3000')
```

You may or may not specify a protocol for the URL endpoint.

Elysia will append the endpoints automatically as follows:

1. If a protocol is specified, use the URL directly
2. If the URL is localhost and ENV is not production, use http
3. Otherwise, use https

This also applies to WebSocket for determining between **ws://** or **wss://**.

***

### Elysia Instance

If an Elysia instance is passed, Eden Treaty will create a `Request` class and pass it to `Elysia.handle` directly without creating a network request.

This allows us to interact with the Elysia server directly without request overhead, or the need to start a server.

```typescript
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .get('/hi', 'Hi Elysia')
    .listen(3000)

const api = treaty(app)
```

If an instance is passed, a generic is not needed as Eden Treaty can infer the type from the parameter directly.

This pattern is recommended for performing unit tests, or creating a type-safe reverse proxy server or microservices.

## Options

2nd optional parameter for Eden Treaty to customize fetch behavior, accepting parameters as follows:

* [fetch](#fetch) - add default parameters to fetch initialization (RequestInit)
* [fetcher](#fetcher) - custom fetch function (e.g., Axios, unfetch)
* [headers](#headers) - define default headers
* [onRequest](#onrequest) - intercept and modify fetch request before firing
* [onResponse](#onresponse) - intercept and modify fetch's response
* [parseDate](#parsedate) - automatically parse date string to Date object
* [throwHttpError](#throwhttperror) - automatically throw an error if the response status is not ok (2xx)

## Fetch

Default parameters appended to the 2nd parameter of fetch extend the type of **Fetch.RequestInit**.

```typescript
export type App = typeof app // [!code ++]
import { treaty } from '@elysia/eden'

treaty<App>('localhost:3000', {
    fetch: {
        credentials: 'include'
    }
})
```

All parameters that are passed to fetch will be passed to the fetcher, which is equivalent to:

```typescript
fetch('http://localhost:3000', {
    credentials: 'include'
})
```

## Fetcher

Provide a custom fetcher function instead of using an environment's default fetch.

```typescript
treaty<App>('localhost:3000', {
    fetcher(url, options) {
        return fetch(url, options)
    }
})
```

It's recommended to replace fetch if you want to use other client other than fetch, eg. Axios, unfetch.

## Headers

Provide additional default headers to fetch; this is a shorthand for `options.fetch.headers`.

```typescript
treaty<App>('localhost:3000', {
    headers: {
        'X-Custom': 'Griseo'
    }
})
```

All parameters that are passed to fetch will be passed to the fetcher, which is equivalent to:

```typescript
fetch('localhost:3000', {
    headers: {
        'X-Custom': 'Griseo'
    }
})
```

headers may accept the following as parameters:

* Object
* Function

### Headers Object

If an object is passed, then it will be passed to fetch directly

```typescript
treaty<App>('localhost:3000', {
    headers: {
        'X-Custom': 'Griseo'
    }
})
```

### Function

You may specify headers as a function to return custom headers based on conditions

```typescript
treaty<App>('localhost:3000', {
    headers(path, options) {
        if(path.startsWith('user'))
            return {
                authorization: 'Bearer 12345'
            }
    }
})
```

You may return an object to append its value to fetch headers.

The headers function accepts 2 parameters:

* path `string` - path which will be sent to the parameter
  * note: hostname will be **excluded**, e.g., (/user/griseo)
* options `RequestInit`: Parameters passed through the 2nd parameter of fetch

### Array

You may define a headers function as an array if multiple conditions are needed.

```typescript
treaty<App>('localhost:3000', {
    headers: [
      (path, options) => {
        if(path.startsWith('user'))
            return {
                authorization: 'Bearer 12345'
            }
        }
    ]
})
```

Eden Treaty will **run all functions** even if the value is already returned.

## Headers Priority

Eden Treaty will prioritize the order headers if duplicated as follows:

1. Inline method - Passed in method function directly
2. headers - Passed in `config.headers`

* If `config.headers` is array, parameters that come after will be prioritized

3. fetch - Passed in `config.fetch.headers`

For example:

```typescript
const api = treaty<App>('localhost:3000', {
    headers: {
        authorization: 'Bearer Aponia'
    }
})

api.profile.get({
    headers: {
        authorization: 'Bearer Griseo'
    }
})
```

This will result in:

```typescript
fetch('http://localhost:3000', {
    headers: {
        authorization: 'Bearer Griseo'
    }
})
```

If the inline function doesn't specify headers, then the result will be "**Bearer Aponia**" instead.

## OnRequest

Intercept and modify the fetch request before firing.

You may return an object to append the value to **RequestInit**.

```typescript
treaty<App>('localhost:3000', {
    onRequest(path, options) {
        if(path.startsWith('user'))
            return {
                headers: {
                    authorization: 'Bearer 12345'
                }
            }
    }
})
```

If value is returned, Eden Treaty will perform a **shallow merge** for returned value and `value.headers`.

**onRequest** accepts 2 parameters:

* path `string` - path which will be sent to parameter
  * note: hostname will be **exclude** eg. (/user/griseo)
* options `RequestInit`: Parameters that passed through 2nd parameter of fetch

### Array

You may define an onRequest function as an array if multiples conditions are need.

```typescript
treaty<App>('localhost:3000', {
    onRequest: [
      (path, options) => {
        if(path.startsWith('user'))
            return {
                headers: {
                    authorization: 'Bearer 12345'
                }
            }
        }
    ]
})
```

Eden Treaty will **run all functions** even if the value is already returned.

## onResponse

Intercept and modify fetch's response or return a new value.

```typescript
treaty<App>('localhost:3000', {
    onResponse(response) {
        if(response.ok)
            return response.json()
    }
})
```

**onRequest** accepts 1 parameter:

* response `Response` - Web Standard Response normally returned from `fetch`

### Array

You may define an onResponse function as an array if multiple conditions are need.

```typescript
treaty<App>('localhost:3000', {
    onResponse: [
        (response) => {
            if(response.ok)
                return response.json()
        }
    ]
})
```

Unlike [headers](#headers) and [onRequest](#onrequest), Eden Treaty will loop through functions until a returned value is found or error thrown, the returned value will be use as a new response.

## parseDate

* default: `true`

Automatically parse date string to Date object.

```typescript
treaty<App>('localhost:3000', {
	parseDate: true
})
```

## throwHttpError

* default: `false`

Automatically throw an error if the response status is not ok (2xx).

```typescript
treaty<App>('localhost:3000', {
	throwHttpError: true
})
```

By default, Eden will not throw an error and return as `{ error }` instead if the response status is not ok (2xx).

You can also specify a custom error handler as follows:

```typescript
treaty<App>('localhost:3000', {
	throwHttpError: (response) => {
		return response.status === 418
	}
})
```

If `throwHttpError` return `true`, Eden will throw an error, otherwise it will return as `{ error }` instead.

---

---
url: 'https://elysiajs.com/eden/treaty/legacy.md'
---

# Eden Treaty Legacy

::: tip NOTE
This is the documentation for Eden Treaty 1 (edenTreaty).

For a new project, we recommend starting with Eden Treaty 2 (treaty) instead.
:::

Eden Treaty is an object-like representation of an Elysia server.

It provides accessors like a normal object with types directly from the server, helping us to move faster and ensuring that nothing breaks.

***

To use Eden Treaty, first export your existing Elysia server's type:

```typescript
// server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]
```

Then import the server type, and consume the Elysia API on client:

```typescript
// client.ts
import { edenTreaty } from '@elysia/eden'
import type { App } from './server' // [!code ++]

const app = edenTreaty<App>('http://localhost:')

// response type: 'Hi Elysia'
const { data: pong, error } = app.get()

// response type: 1895
const { data: id, error } = app.id['1895'].get()

// response type: { id: 1895, name: 'Skadi' }
const { data: nendoroid, error } = app.mirror.post({
    id: 1895,
    name: 'Skadi'
})
```

::: tip
Eden Treaty is fully type-safe with auto-completion support.
:::

## Anatomy

Eden Treaty will transform all existing paths to an object-like representation that can be described as:

```typescript
EdenTreaty.<1>.<2>.<n>.<method>({
    ...body,
    $query?: {},
    $fetch?: RequestInit
})
```

### Path

Eden will transform `/` into `.` which can be called with a registered `method`, for example:

* **/path** -> .path
* **/nested/path** -> .nested.path

### Path parameters

Path parameters will be mapped automatically by their name in the URL.

* **/id/:id** -> .id.`<anyThing>`
* eg: .id.hi
* eg: .id\['123']

::: tip
If a path doesn't support path parameters, TypeScript will show an error.
:::

### Query

You can append queries to path with `$query`:

```typescript
app.get({
    $query: {
        name: 'Eden',
        code: 'Gold'
    }
})
```

### Fetch

Eden Treaty is a fetch wrapper, you can add any valid [Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) parameters to Eden by passing it to `$fetch`:

```typescript
app.post({
    $fetch: {
        headers: {
            'x-organization': 'MANTIS'
        }
    }
})
```

## Error Handling

Eden Treaty will return a value of `data` and `error` as a result, both fully typed.

```typescript
// response type: { id: 1895, name: 'Skadi' }
const { data: nendoroid, error } = app.mirror.post({
    id: 1895,
    name: 'Skadi'
})

if(error) {
    switch(error.status) {
        case 400:
        case 401:
            warnUser(error.value)
            break

        case 500:
        case 502:
            emergencyCallDev(error.value)
            break

        default:
            reportError(error.value)
            break
    }

    throw error
}

const { id, name } = nendoroid
```

Both **data** and **error** will be typed as nullable until you can confirm their statuses with a type guard.

To put it simply, if the fetch is successful, data will have a value and error will be null, and vice versa.

::: tip
The error is wrapped with an `Error`, and its value returned from the server can be retrieved from `Error.value`
:::

### Error type based on status

Both Eden Treaty and Eden Fetch can narrow down an error type based on status code if you explicitly provide an error type in the Elysia server.

```typescript
// server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .model({
        nendoroid: t.Object({
            id: t.Number(),
            name: t.String()
        }),
        error: t.Object({
            message: t.String()
        })
    })
    .get('/', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: 'nendoroid',
        response: {
            200: 'nendoroid', // [!code ++]
            400: 'error', // [!code ++]
            401: 'error' // [!code ++]
        }
    })
    .listen(3000)

export type App = typeof app
```

And on the client side:

```typescript
const { data: nendoroid, error } = app.mirror.post({
    id: 1895,
    name: 'Skadi'
})

if(error) {
    switch(error.status) {
        case 400:
        case 401:
            // narrow down to type 'error' described in the server
            warnUser(error.value)
            break

        default:
            // typed as unknown
            reportError(error.value)
            break
    }

    throw error
}
```

## WebSocket

Eden supports WebSocket using the same API as a normal route.

```typescript
// Server
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .ws('/chat', {
        message(ws, message) {
            ws.send(message)
        },
        body: t.String(),
        response: t.String()
    })
    .listen(3000)

type App = typeof app
```

To start listening to real-time data, call the `.subscribe` method:

```typescript
// Client
import { edenTreaty } from '@elysia/eden'
const app = edenTreaty<App>('http://localhost:')

const chat = app.chat.subscribe()

chat.subscribe((message) => {
    console.log('got', message)
})

chat.send('hello from client')
```

We can use [schema](/integrations/cheat-sheet#schema) to enforce type-safety on WebSockets, just like a normal route.

***

**Eden.subscribe** returns **EdenWebSocket** which extends the [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/WebSocket) class with type-safety. The syntax is identical to WebSocket.

If more control is needed, **EdenWebSocket.raw** can be accessed to interact with the native WebSocket API.

## File Upload

You may pass any of the following to the field to attach a file:

* **File**
* **FileList**
* **Blob**

Attaching a file will result in **content-type** being **multipart/form-data**

Suppose we have the server as follows:

```typescript
// server.ts
import { Elysia } from 'elysia'

const app = new Elysia()
    .post('/image', ({ body: { image, title } }) => title, {
        body: t.Object({
            title: t.String(),
            image: t.Files(),
        })
    })
    .listen(3000)

export type App = typeof app
```

We can use the client as follows:

```typescript
// client.ts
import { edenTreaty } from '@elysia/eden'
import type { Server } from './server'

export const client = edenTreaty<Server>('http://localhost:3000')

const id = <T extends HTMLElement = HTMLElement>(id: string) =>
    document.getElementById(id)! as T

const { data } = await client.image.post({
    title: "Misono Mika",
    image: id<HTMLInputElement>('picture').files!,
})
```

---

---
url: 'https://elysiajs.com/eden/treaty/parameters.md'
---

# Parameters

We need to send a payload to the server eventually.

To handle this, Eden Treaty's methods accept 2 parameters to send data to the server.

Both parameters are type-safe and will be guided by TypeScript automatically:

1. body
2. additional parameters
   * query
   * headers
   * fetch

```typescript
import { Elysia, t } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .post('/user', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })
    .listen(3000)

const api = treaty<typeof app>('localhost:3000')

// ✅ works
api.user.post({
    name: 'Elysia'
})

// ✅ also works
api.user.post({
    name: 'Elysia'
}, {
    // This is optional as not specified in schema
    headers: {
        authorization: 'Bearer 12345'
    },
    query: {
        id: 2
    }
})
```

Unless the method doesn't accept a body, then the body will be omitted and left with a single parameter only.

If the method is **"GET"** or **"HEAD"**:

1. Additional parameters
   * query
   * headers
   * fetch

```typescript
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .get('/hello', () => 'hi')
    .listen(3000)

const api = treaty<typeof app>('localhost:3000')

// ✅ works
api.hello.get({
    // This is optional as not specified in schema
    headers: {
        hello: 'world'
    }
})
```

## Empty body

If the body is optional or not needed, but query or headers are required, you may pass the body as `null` or `undefined` instead.

```typescript
import { Elysia, t } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .post('/user', () => 'hi', {
        query: t.Object({
            name: t.String()
        })
    })
    .listen(3000)

const api = treaty<typeof app>('localhost:3000')

api.user.post(null, {
    query: {
        name: 'Ely'
    }
})
```

## Fetch parameters

Eden Treaty is a fetch wrapper; we may add any valid [Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) parameters to Eden by passing them to `$fetch`:

```typescript
import { Elysia, t } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .get('/hello', () => 'hi')
    .listen(3000)

const api = treaty<typeof app>('localhost:3000')

const controller = new AbortController()

const cancelRequest = setTimeout(() => {
    controller.abort()
}, 5000)

await api.hello.get({
    fetch: {
        signal: controller.signal
    }
})

clearTimeout(cancelRequest)
```

## File Upload

We may pass any of the following to attach file(s):

* **File**
* **File\[]**
* **FileList**
* **Blob**

Attaching a file will result in **content-type** being **multipart/form-data**

Suppose we have the server as follows:

```typescript
import { Elysia, t } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .post('/image', ({ body: { image, title } }) => title, {
        body: t.Object({
            title: t.String(),
            image: t.Files()
        })
    })
    .listen(3000)

export const api = treaty<typeof app>('localhost:3000')

const images = document.getElementById('images') as HTMLInputElement

const { data } = await api.image.post({
    title: "Misono Mika",
    image: images.files!,
})
```

---

---
url: 'https://elysiajs.com/eden/treaty/response.md'
---

# Response

Once the fetch method is called, Eden Treaty returns a `Promise` containing an object with the following properties:

* data - returned value of the response (2xx)
* error - returned value from the response (>= 3xx)
* response `Response` - Web Standard Response class
* status `number` - HTTP status code
* headers `FetchRequestInit['headers']` - response headers

Once returned, you must provide error handling to ensure that the response data value is unwrapped; otherwise, the value will be nullable. Elysia provides an `error()` helper function to handle the error, and Eden will provide type narrowing for the error value.

```typescript
import { Elysia, t } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
    .post('/user', ({ body: { name }, status }) => {
        if(name === 'Otto') return status(400)

        return name
    }, {
        body: t.Object({
            name: t.String()
        })
    })
    .listen(3000)

const api = treaty<typeof app>('localhost:3000')

const submit = async (name: string) => {
    const { data, error } = await api.user.post({
        name
    })

    // type: string | null
    console.log(data)

    if (error)
        switch(error.status) {
            case 400:
                // Error type will be narrow down
                throw error.value

            default:
                throw error.value
        }

    // Once the error is handled, type will be unwrapped
    // type: string
    return data
}
```

By default, Elysia infers `error` and `response` types to TypeScript automatically, and Eden will be providing auto-completion and type narrowing for accurate behavior.

::: tip
If the server responds with an HTTP status >= 300, then the value will always be `null`, and `error` will have a returned value instead.

Otherwise, response will be passed to `data`.
:::

## Stream response

Eden will interpret a stream response or [Server-Sent Events](/essential/handler.html#server-sent-events-sse) as an `AsyncGenerator`, allowing us to use a `for await` loop to consume the stream.

::: code-group

```typescript twoslash [Stream]
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
	.get('/ok', function* () {
		yield 1
		yield 2
		yield 3
	})

const { data, error } = await treaty(app).ok.get()
if (error) throw error

for await (const chunk of data)
	console.log(chunk)
               // ^?
```

```typescript twoslash [Server-Sent Events]
import { Elysia, sse } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
	.get('/ok', function* () {
		yield sse({
			event: 'message',
			data: 1
		})
		yield sse({
			event: 'message',
			data: 2
		})
		yield sse({
			event: 'end'
		})
	})

const { data, error } = await treaty(app).ok.get()
if (error) throw error

for await (const chunk of data)
	console.log(chunk)
               // ^?







//
```

:::

## Utility types

Eden Treaty provides utility types `Treaty.Data<T>` and `Treaty.Error<T>` to extract the `data` and `error` types from the response.

```typescript twoslash
import { Elysia, t } from 'elysia'

import { treaty, Treaty } from '@elysia/eden'

const app = new Elysia()
	.post('/user', ({ body: { name }, status }) => {
		if(name === 'Otto') return status(400)

		return name
	}, {
		body: t.Object({
			name: t.String()
		})
	})
	.listen(3000)

const api =
	treaty<typeof app>('localhost:3000')

type UserData = Treaty.Data<typeof api.user.post>
//     ^?


// Alternatively, you can also pass a response
const response = await api.user.post({
	name: 'Saltyaom'
})

type UserDataFromResponse = Treaty.Data<typeof response>
//     ^?



type UserError = Treaty.Error<typeof api.user.post>
//     ^?












//
```

---

---
url: 'https://elysiajs.com/eden/treaty/unit-test.md'
---

# Unit Test

According to [Eden Treaty config](/eden/treaty/config.html#urlorinstance) and [Unit Test](/patterns/unit-test), we may pass an Elysia instance to Eden Treaty directly to interact with the Elysia server directly without sending a network request.

We may use this pattern to create a unit test with end-to-end type safety and type-level tests all at once.

```typescript twoslash
// test/index.test.ts
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia().get('/hello', 'hi')
const api = treaty(app)

describe('Elysia', () => {
    it('returns a response', async () => {
        const { data } = await api.hello.get()

        expect(data).toBe('hi')
              // ^?

    })
})
```

## Type safety test

To perform a type safety test, simply run **tsc** on test folders.

```bash
tsc --noEmit test/**/*.ts
```

This is useful to ensure type integrity for both client and server, especially during migrations.

---

---
url: 'https://elysiajs.com/eden/treaty/websocket.md'
---

# WebSocket

Eden Treaty supports WebSocket using the `subscribe` method.

```typescript
import { Elysia, t } from "elysia";
import { treaty } from "@elysia/eden";

const app = new Elysia()
  .ws("/chat", {
    body: t.String(),
    response: t.String(),
    message(ws, message) {
      ws.send(message);
    },
  })
  .listen(3000);

const api = treaty<typeof app>("localhost:3000");

const chat = api.chat.subscribe();

chat.subscribe((message) => {
  console.log("got", message);
});

chat.on("open", () => {
  chat.send("hello from client");
});
```

**.subscribe** accepts the same parameters as `get` and `head`.

## Response

**Eden.subscribe** returns **EdenWS** which extends the [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/WebSocket), resulting in identical syntax.

If more control is needed, **EdenWebSocket.raw** can be accessed to interact with the native WebSocket API.

---

---
url: 'https://elysiajs.com/illust.md'
---


---

---
url: 'https://elysiajs.com/tutorial/getting-started/encapsulation.md'
---

# Encapsulation

Elysia hooks are **encapsulated** to its own instance only.

If you create a new instance, it will not share hooks with other instances.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(
		({ query: { name }, status }) => {
			if(!name)
				return status(401)
		}
	)
	.get('/profile', () => 'Hi!')

new Elysia()
	.use(profile)
	.patch('/rename', () => 'Ok! XD')
	.listen(3000)
```

> Try changing the path in the URL bar to **/rename** and see the result

**Elysia isolates lifecycle** unless explicitly stated.

This is similar to **export** in JavaScript, where you need to export the function to make it available outside the module.

To **"export"** the lifecycle to other instances, you must specify the scope.

### Scope

There are 3 scopes available:

1. **local** (default) - apply to only current instance and descendant only
2. **scoped** - apply to parent, current instance and descendants
3. **global** - apply to all instance that apply the plugin (all parents, current, and descendants)

In our case, we want to apply the sign-in check to the `app` which is a direct parent, so we can use either **scoped** or **global**.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(
		{ as: 'scoped' }, // [!code ++]
		({ cookie }) => {
			throwIfNotSignIn(cookie)
		}
	)
	.get('/profile', () => 'Hi there!')

const app = new Elysia()
	.use(profile)
	// This has sign in check
	.patch('/rename', ({ body }) => updateProfile(body))
```

Casting lifecycle to **"scoped"** will export lifecycle to **parent instance**.
While **"global"** will export lifecycle to **all instances** that has a plugin.

Learn more about this in scope.

## Guard

Similar to lifecycle, **schema** is also encapsulated to its own instance.

We can specify guard scope similar to lifecycle.

```typescript
import { Elysia } from 'elysia'

const user = new Elysia()
	.guard({
		as: 'scoped', // [!code ++]
		query: t.Object({
			age: t.Number(),
			name: t.Optional(t.String())
		}),
		beforeHandle({ query: { age }, status }) {
			if(age < 18) return status(403)
		}
	})
	.get('/profile', () => 'Hi!')
	.get('/settings', () => 'Settings')
```

It's very important to note that every hook will affect all routes **after** its declaration.

See Scope for more information.

## Assignment

Let's define a scope for `nameCheck`, and `ageCheck` to make our app works.

\<template #answer>

We can modify scope as follows:

1. modify `nameCheck` scope to **scoped**
2. modify `ageCheck` scope to **global**

```typescript
import { Elysia, t } from 'elysia'

const nameCheck = new Elysia()
	.onBeforeHandle(
		{ as: 'scoped' }, // [!code ++]
		({ query: { name }, status }) => {
			if(!name) return status(401)
		}
	)

const ageCheck = new Elysia()
	.guard({
		as: 'global', // [!code ++]
		query: t.Object({
			age: t.Number(),
			name: t.Optional(t.String())
		}),
		beforeHandle({ query: { age }, status }) {
			if(age < 18) return status(403)
		}
	})

const name = new Elysia()
	.use(nameCheck)
	.patch('/rename', () => 'Ok! XD')

const profile = new Elysia()
	.use(ageCheck)
	.use(name)
	.get('/profile', () => 'Hi!')

new Elysia()
	.use(profile)
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/tutorial/features/end-to-end-type-safety.md'
---

# End-to-End Type Safety

Elysia provides an end-to-end type safety between backend and frontend **without code generation** similar to tRPC, using Eden.

```typescript
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

// Backend
export const app = new Elysia()
	.get('/', 'Hello Elysia!')
	.listen(3000)

// Frontend
const client = treaty<typeof app>('localhost:3000')

const { data, error } = await client.get()

console.log(data) // Hello World
```

This works by inferring the types from the Elysia instance, and uses type hints to provide type safety for the client.

See Eden Treaty.

## Assignment

Let's click the  icon in the preview to see how's the request is logged.

---

---
url: 'https://elysiajs.com/eden/overview.md'
---

# End-to-End Type Safety&#x20;

Imagine you have a toy train set.

Each piece of the train track has to fit perfectly with the next one, like puzzle pieces.

End-to-end type safety is like making sure all the pieces of the track match up correctly so the train doesn't fall off or get stuck.

For a framework to have end-to-end type safety means that you can connect the client and server in a type-safe manner.

Elysia provides end-to-end type safety **without code generation** out of the box with an RPC-like connector, **Eden**.

Other frameworks that support e2e type safety:

* tRPC
* Remix
* SvelteKit
* Nuxt
* TS-Rest

Elysia allows you to change the type on the server, and it will be instantly reflected on the client, helping with auto-completion and type enforcement.

## Eden

Eden is an RPC-like client to connect Elysia with **end-to-end type safety** using only TypeScript's type inference instead of code generation.

It allows you to sync client and server types effortlessly, weighing less than 2KB.

Eden consists of 2 modules:

1. Eden Treaty **(recommended)**: an improved RPC version of Eden Treaty 1 (edenTreaty)
2. Eden Fetch: A fetch-like client with type safety

Below is an overview, use cases, and a comparison for each module.

## Eden Treaty (Recommended)

Eden Treaty is an object-like representation of an Elysia server providing end-to-end type safety and a significantly improved developer experience.

With Eden Treaty, we can interact with an Elysia server with full-type support and auto-completion, error handling with type narrowing, and create type-safe unit tests.

Example usage of Eden Treaty:

```typescript twoslash
// @filename: server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/', 'hi')
    .get('/users', () => 'Skadi')
    .put('/nendoroid/:id', ({ body }) => body, {
        body: t.Object({
            name: t.String(),
            from: t.String()
        })
    })
    .get('/nendoroid/:id/name', () => 'Skadi')
    .listen(3000)

export type App = typeof app

// @filename: index.ts
// ---cut---
import { treaty } from '@elysia/eden'
import type { App } from './server'

const app = treaty<App>('localhost:3000')

// @noErrors
app.
//  ^|




// Call [GET] at '/'
const { data } = await app.get()

// Call [PUT] at '/nendoroid/:id'
const { data: nendoroid, error } = await app.nendoroid({ id: 1895 }).put({
    name: 'Skadi',
    from: 'Arknights'
})
```

## Eden Fetch

A fetch-like alternative to Eden Treaty for developers who prefer fetch syntax.

```typescript
import { edenFetch } from '@elysia/eden'
import type { App } from './server'

const fetch = edenFetch<App>('http://localhost:3000')

const { data } = await fetch('/name/:name', {
    method: 'POST',
    params: {
        name: 'Saori'
    },
    body: {
        branch: 'Arius',
        type: 'Striker'
    }
})
```

::: tip NOTE
Unlike Eden Treaty, Eden Fetch doesn't provide WebSocket implementation for the Elysia server.
:::

---

---
url: 'https://elysiajs.com/tutorial/patterns/error-handling.md'
---

# Error Handling

onError is called when an **error is thrown**.

It accepts **context** similar to a handler but includes an additional:

* error - a thrown error
* code - error code

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onError(({ code, status }) => {
		if(code === "NOT_FOUND")
			return 'uhe~ are you lost?'

		return status(418, "My bad! But I'm cute so you'll forgive me, right?")
	})
	.get('/', () => 'ok')
	.listen(3000)
```

You can return a status to override the default error status.

## Custom Error

You can provide a custom error with error code as follows:

```typescript
import { Elysia } from 'elysia'

class NicheError extends Error {
	constructor(message: string) {
		super(message)
	}
}

new Elysia()
	.error({ // [!code ++]
		'NICHE': NicheError // [!code ++]
	}) // [!code ++]
	.onError(({ error, code, status }) => {
		if(code === 'NICHE') {
			// Typed as NicheError
			console.log(error)

			return status(418, "We have no idea how you got here")
		}
	})
	.get('/', () => {
        throw new NicheError('Custom error message')
	})
	.listen(3000)
```

Elysia uses error codes to narrow down the type of error.

It's recommended to register custom errors as Elysia can narrow down the type.

### Error Status Code

You can also provide a custom status code by adding a **status** property to class:

```typescript
import { Elysia } from 'elysia'

class NicheError extends Error {
	status = 418 // [!code ++]

	constructor(message: string) {
		super(message)
	}
}
```

Elysia will use this status code if the error is thrown, see Custom Status Code.

### Error Response

You can also define a custom error response directly into the error by providing a `toResponse` method:

```typescript
import { Elysia } from 'elysia'

class NicheError extends Error {
	status = 418

	constructor(message: string) {
		super(message)
	}

	toResponse() { // [!code ++]
		return { message: this.message } // [!code ++]
	} // [!code ++]
}
```

Elysia will use this response if the error is thrown, see Custom Error Response.

## Assignment

Let's try to extend Elysia's context.

\<template #answer>

1. You can narrow down the error by "NOT\_FOUND" to override 404 response.
2. Provide your error to `.error()` method with status property of 418.

```typescript
import { Elysia } from 'elysia'

class YourError extends Error {
	status = 418

	constructor(message: string) {
		super(message)
	}
}

new Elysia()
	.error({
		"YOUR_ERROR": YourError
	})
	.onError(({ code, status }) => {
		if(code === "NOT_FOUND")
			return "Hi there"
	})
	.get('/', () => {
		throw new YourError("A")
	})
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/patterns/error-handling.md'
---

# Error Handling&#x20;

This page provides a more advanced guide for effectively handling errors with Elysia.

If you haven't read **"Life Cycle (onError)"** yet, we recommend you to read it first.

## Custom Validation Message

When defining a schema, you can provide a custom validation message for each field.

This message will be returned as-is when the validation fails.

```ts
import { Elysia } from 'elysia'

new Elysia().get('/:id', ({ params: { id } }) => id, {
    params: t.Object({
        id: t.Number({
            error: 'id must be a number' // [!code ++]
        })
    })
})
```

If the validation fails on the `id` field, the response will be returned as `id must be a number`.

### Validation Detail&#x20;

Returning a value from `schema.error` will return the validation as-is, but sometimes you may also want to return the validation details, such as the field name and the expected type

You can do this by using the `validationDetail` option.

```ts
import { Elysia, validationDetail } from 'elysia' // [!code ++]

new Elysia().get('/:id', ({ params: { id } }) => id, {
    params: t.Object({
        id: t.Number({
            error: validationDetail('id must be a number') // [!code ++]
        })
    })
})
```

This will include all of the validation details in the response, such as the field name and the expected type.

But if you plan to use `validationDetail` in every field, adding it manually can be annoying.

You can automatically add validation detail by handling it in `onError` hook.

```ts
new Elysia()
    .onError(({ error, code }) => {
        if (code === 'VALIDATION') return error.detail(error.message) // [!code ++]
    })
    .get('/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number({
                error: 'id must be a number'
            })
        })
    })
    .listen(3000)
```

This will apply every validation error with a custom message with custom validation message.

## Validation Detail on production

By default, Elysia will omit all validation detail if `NODE_ENV` is `production`.

This is done to prevent leaking sensitive information about the validation schema, such as field names and expected types, which could be exploited by an attacker.

Elysia will only return that validation failed without any details.

```json
{
    "type": "validation",
    "on": "body",
    "found": {},
    // Only shown for custom error
    "message": "x must be a number"
}
```

The `message` property is optional and is omitted by default unless you provide a custom error message in the schema.

This can be overridden by setting `Elysia.allowUnsafeValidationDetails` to `true`, see [Elysia configuration](/patterns/configuration#allow-unsafe-validation-details) for more details.

## Custom Error

Elysia supports custom errors both in the type-level and implementation level.

By default, Elysia has a set of built-in error types like `VALIDATION`, `NOT_FOUND` which will narrow down the type automatically.

If Elysia doesn't know the error, the error code will be `UNKNOWN` with default status of `500`

But you can also add a custom error with type safety with `Elysia.error` which will help narrow down the error type for full type safety with auto-complete, and custom status code as follows:

```typescript
import { Elysia } from 'elysia'

class MyError extends Error {
    constructor(public message: string) {
        super(message)
    }
}

new Elysia()
    .error({
        MyError
    })
    .onError(({ code, error }) => {
        switch (code) {
            // With auto-completion
            case 'MyError':
                // With type narrowing
                // Hover to see error is typed as `CustomError`
                return error
        }
    })
    .get('/:id', () => {
        throw new MyError('Hello Error')
    })
```

### Custom Status Code

You can also provide a custom status code for your custom error by adding `status` property in your custom error class.

```typescript
import { Elysia } from 'elysia'

class MyError extends Error {
    status = 418

    constructor(public message: string) {
        super(message)
    }
}
```

Elysia will then use this status code when the error is thrown.

Otherwise you can also set the status code manually in the `onError` hook.

```typescript
import { Elysia } from 'elysia'

class MyError extends Error {
	constructor(public message: string) {
		super(message)
	}
}

new Elysia()
	.error({
		MyError
	})
	.onError(({ code, error, status }) => {
		switch (code) {
			case 'MyError':
				return status(418, error.message)
		}
	})
	.get('/:id', () => {
		throw new MyError('Hello Error')
	})
```

### Custom Error Response

You can also provide a custom `toResponse` method in your custom error class to return a custom response when the error is thrown.

```typescript
import { Elysia } from 'elysia'

class MyError extends Error {
	status = 418

	constructor(public message: string) {
		super(message)
	}

	toResponse() {
		return Response.json({
			error: this.message,
			code: this.status
		}, {
			status: 418
		})
	}
}
```

## To Throw or Return

Most error handling in Elysia can be done by throwing an error and will be handled in `onError`.

But for `status` it can be a little bit confusing, since it can be used both as a return value or throw an error.

It could either be **return** or **throw** based on your specific needs.

* If a `status` is **throw**, it will be caught by `onError` middleware.
* If a `status` is **return**, it will be **NOT** caught by `onError` middleware.

See the following code:

```typescript
import { Elysia, file } from 'elysia'

new Elysia()
    .onError(({ code, error, path }) => {
        if (code === 418) return 'caught'
    })
    .get('/throw', ({ status }) => {
        // This will be caught by onError
        throw status(418)
    })
    .get('/return', ({ status }) => {
        // This will NOT be caught by onError
        return status(418)
    })
```

Here we use `status(418)` which is the "I'm a teapot" status code. You can also use the string name directly: `status("I'm a teapot")`. See Status for more on using status codes.

---

---
url: 'https://elysiajs.com/patterns/extends-context.md'
---

# Extend context&#x20;

Elysia provides a minimal Context by default, allowing us to extend Context for our specific need using state, decorate, derive, and resolve.

Elysia allows us to extend Context for various use cases like:

* extracting user ID as variable
* injecting a common repository pattern
* adding a database connection

We may extend Elysia's context by using the following APIs to customize the Context:

* [state](#state) - a global mutable state
* [decorate](#decorate) - additional property assigned to **Context**
* [derive](#derive) / [resolve](#resolve) - create a new value from existing property

### When to extend context

You should only extend context when:

* A property is a global mutable state, and shared across multiple routes using [state](#state)
* If a property is associated with a request or response using [decorate](#decorate)
* A property is derived from an existing property using [derive](#derive) / [resolve](#resolve)

Otherwise, we recommend defining a value or function separately than extending the context.

::: tip
It's recommended to assign properties related to request and response, or frequently used functions to Context for separation of concerns.
:::

## State

**State** is a global mutable object or state shared across the Elysia app.

Once **state** is called, value will be added to **store** property **once at call time**, and can be used in handler.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .state('version', 1)
    .get('/a', ({ store: { version } }) => version)
                // ^?
    .get('/b', ({ store }) => store)
    .get('/c', () => 'still ok')
    .listen(3000)
```

### When to use

* When you need to share a primitive mutable value across multiple routes
* If you want to use a non-primitive or a `wrapper` value or class that mutate an internal state, use [decorate](#decorate) instead.

### Key takeaway

* **store** is a representation of a single-source-of-truth global mutable object for the entire Elysia app.
* **state** is a function to assign an initial value to **store**, which could be mutated later.
* Make sure to assign a value before using it in a handler.

```typescript twoslash
// @errors: 2339
import { Elysia } from 'elysia'

new Elysia()
    // ❌ TypeError: counter doesn't exist in store
    .get('/error', ({ store }) => store.counter)
    .state('counter', 0)
    // ✅ Because we assigned a counter before, we can now access it
    .get('/', ({ store }) => store.counter)
```

::: tip
Beware that we cannot use a state value before assign.

Elysia registers state values into the store automatically without explicit type or additional TypeScript generic needed.
:::

### Reference and value Gotcha

To mutate the state, it's recommended to use **reference** to mutate rather than using an actual value.

When accessing the property from JavaScript, if we define a primitive value from an object property as a new value, the reference is lost, the value is treated as new separate value instead.

For example:

```typescript
const store = {
    counter: 0
}

store.counter++
console.log(store.counter) // ✅ 1
```

We can use **store.counter** to access and mutate the property.

However, if we define a counter as a new value

```typescript
const store = {
    counter: 0
}

let counter = store.counter

counter++
console.log(store.counter) // ❌ 0
console.log(counter) // ✅ 1
```

Once a primitive value is redefined as a new variable, the reference **"link"** will be missing, causing unexpected behavior.

This can apply to `store`, as it's a global mutable object instead.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .state('counter', 0)
    // ✅ Using reference, value is shared
    .get('/', ({ store }) => store.counter++)
    // ❌ Creating a new variable on primitive value, the link is lost
    .get('/error', ({ store: { counter } }) => counter)
```

## Decorate

**decorate** assigns an additional property to **Context** directly **at call time**.

```typescript
import { Elysia } from 'elysia'

class Logger {
    log(value: string) {
        console.log(value)
    }
}

new Elysia()
    .decorate('logger', new Logger())
    // ✅ defined from the previous line
    .get('/', ({ logger }) => {
        logger.log('hi')

        return 'hi'
    })
```

### When to use

* A constant or readonly value object to **Context**
* Non-primitive value or class that may contain internal mutable state
* Additional functions, singletons, or immutable property to all handlers.

### Key takeaway

* Unlike **state**, decorated value **SHOULD NOT** be mutated although it's possible
* Make sure to assign a value before using it in a handler.

## Derive

###### ⚠️ Derive doesn't handle type integrity, you might want to use [resolve](#resolve) instead.

Retrieve values from existing properties in **Context** and assign new properties.

Derive assigns when request happens **at transform lifecycle** allowing us to "derive" (create new properties from existing properties).

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .derive(({ headers }) => {
        const auth = headers['authorization']

        return {
            bearer: auth?.startsWith('Bearer ') ? auth.slice(7) : null
        }
    })
    .get('/', ({ bearer }) => bearer)
```

Because **derive** is assigned once a new request starts, **derive** can access request properties like **headers**, **query**, **body** where **store**, and **decorate** can't.

### When to use

* Create a new property from existing properties in **Context** without validation or type checking
* When you need to access request properties like **headers**, **query**, **body** without validation

### Key takeaway

* Unlike **state** and **decorate** instead of assigning **at call time**, **derive** is assigned once a new request starts.
* **derive is called at transform, or before validation** occurs, Elysia cannot safely confirm the type of request property resulting in as **unknown**. If you want to assign a new value from typed request properties, you may want to use [resolve](#resolve) instead.

## Resolve

Similar as [derive](#derive) but ensure type integrity.

Resolve allow us to assign a new property to context.

Resolve is called at **beforeHandle** lifecycle or **after validation**, allowing us to **resolve** request properties safely.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.guard({
		headers: t.Object({
			bearer: t.String({
				pattern: '^Bearer .+$'
			})
		})
	})
	.resolve(({ headers }) => {
		return {
			bearer: headers.bearer.slice(7)
		}
	})
	.get('/', ({ bearer }) => bearer)
```

### When to use

* Create a new property from existing properties in **Context** with type integrity (type checked)
* When you need to access request properties like **headers**, **query**, **body** with validation

### Key takeaway

* **resolve is called at beforeHandle, or after validation** happens. Elysia can safely confirm the type of request property resulting in as **typed**.

### Error from resolve/derive

As resolve and derive is based on **transform** and **beforeHandle** lifecycle, we can return an error from resolve and derive. If error is returned from **derive**, Elysia will return early exit and return the error as response.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .derive(({ headers, status }) => {
        const auth = headers['authorization']

        if(!auth) return status(400)

        return {
            bearer: auth?.startsWith('Bearer ') ? auth.slice(7) : null
        }
    })
    .get('/', ({ bearer }) => bearer)
```

## Pattern Advanced Concept

**state**, **decorate** offers a similar API pattern for assigning property to Context as the following:

* key-value
* object
* remap

Where **derive** can be only used with **remap** because it depends on existing value.

### key-value

We can use **state**, and **decorate** to assign a value using a key-value pattern.

```typescript
import { Elysia } from 'elysia'

class Logger {
    log(value: string) {
        console.log(value)
    }
}

new Elysia()
    .state('counter', 0)
    .decorate('logger', new Logger())
```

This pattern is great for readability for setting a single property.

### Object

Assigning multiple properties is better contained in an object for a single assignment.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .decorate({
        logger: new Logger(),
        trace: new Trace(),
        telemetry: new Telemetry()
    })
```

The object offers a less repetitive API for setting multiple values.

### Remap

Remap is a function reassignment.

Allowing us to create a new value from existing value like renaming or removing a property by providing a function and returning an entirely new object to reassign the value.

By providing a function, and returning an entirely new object to reassign the value.

```typescript twoslash
// @errors: 2339
import { Elysia } from 'elysia'

new Elysia()
    .state('counter', 0)
    .state('version', 1)
    .state(({ version, ...store }) => ({
        ...store,
        elysiaVersion: 1
    }))
    // ✅ Create from state remap
    .get('/elysia-version', ({ store }) => store.elysiaVersion)
    // ❌ Excluded from state remap
    .get('/version', ({ store }) => store.version)
```

It's a good idea to use state remap to create a new initial value from the existing value.

However, it's important to note that Elysia doesn't offer reactivity from this approach, as remap only assigns an initial value.

::: tip
Using remap, Elysia will treat a returned object as a new property, removing any property that is missing from the object.
:::

## Affix Advance Concept

To provide a smoother experience, some plugins might have a lot of property value which can be overwhelming to remap one-by-one.

The **Affix** function which consists of **prefix** and **suffix**, allowing us to remap all properties of an instance.

```ts
import { Elysia } from 'elysia'

const setup = new Elysia({ name: 'setup' })
    .decorate({
        argon: 'a',
        boron: 'b',
        carbon: 'c'
    })

const app = new Elysia()
    .use(setup)
    .prefix('decorator', 'setup')
    .get('/', ({ setupCarbon, ...rest }) => setupCarbon)
```

Allowing us to bulk remap a property of the plugin effortlessly, preventing the name collision of the plugin.

By default, **affix** will handle both runtime, type-level code automatically, remapping the property to camelCase as naming convention.

In some cases, we can also remap all properties of the plugin:

```ts
import { Elysia } from 'elysia'

const setup = new Elysia({ name: 'setup' })
    .decorate({
        argon: 'a',
        boron: 'b',
        carbon: 'c'
    })

const app = new Elysia()
    .use(setup)
    .prefix('all', 'setup') // [!code ++]
    .get('/', ({ setupCarbon, ...rest }) => setupCarbon)
```

---

---
url: 'https://elysiajs.com/tutorial/patterns/extends-context.md'
---

# Extends Context

Elysia provides a context with small utilities to help you get started.

You can extend Elysia's context with:

1. Decorate
2. State
3. Resolve
4. Derive

## Decorate

**Singleton**, and **immutable** properties that are shared across all requests.

```typescript
import { Elysia } from 'elysia'

class Logger {
    log(value: string) {
        console.log(value)
    }
}

new Elysia()
    .decorate('logger', new Logger())
    .get('/', ({ logger }) => {
        logger.log('hi')

        return 'hi'
    })
```

Decorated value it will be available in the context as a read-only property, see Decorate.

## State

A **mutable** reference that is shared across all requests.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.state('count', 0)
	.get('/', ({ store }) => {
		store.count++

		return store.count
	})
```

State will be available in **context.store** that is shared across every request, see State.

## Resolve / Derive

Decorate value is registered as a singleton.

While Resolve, and Derive allows you to abstract a context value **per request**.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.derive(({ headers: { authorization } }) => ({
		authorization
	}))
	.get('/', ({ authorization }) => authorization)
```

Any **returned value will be available in context** except status, which will be send to client directly, and abort the subsequent handlers.

Syntax for both resolve, derive is similar but they have different use cases.

Under the hood, both is a syntax sugar (with type safety) of a lifecycle:

* derive is based on transform
* resolve is based on before handle

Since derive is based on transform, which means that data isn't validated, and coerce/transform yet. It's better to use resolve if you need validated data.

## Scope

State, and Decorate are shared across all requests, and instances.

Resolve, and Derive are per request, and have an encapsulation scope (as they're based on life-cycle event).

If you want to use a resolved/derived value from a plugin, you would have to declare a Scope.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
	.derive(
		{ as: 'scoped' }, // [!code ++]
		({ headers: { authorization } }) => ({
			authorization
		})
	)

new Elysia()
	.use(plugin)
	.get('/', ({ authorization }) => authorization)
	.listen(3000)
```

## Assignment

Let's try to extend Elysia's context.

\<template #answer>

We can use resolve to extract age from query.

```typescript
import { Elysia, t } from 'elysia'

class Logger {
	log(info: string) {
		console.log(info)
	}
}

new Elysia()
	.decorate('logger', new Logger())
	.onRequest(({ request, logger }) => {
		logger.log(`Request to ${request.url}`)
	})
	.guard({
		query: t.Optional(
			t.Object({
				age: t.Number({ min: 15 })
			})
		)
	})
	.resolve(({ query: { age }, status }) => {
		if(!age) return status(401)

		return { age }
	})
	.get('/profile', ({ age }) => age)
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/patterns/fullstack-dev-server.md'
---

# Elysia with Bun Fullstack Dev Server

Bun 1.3 introduces a [Fullstack Dev Server](https://bun.com/docs/bundler/fullstack) with HMR support.

This allows us to directly use React without any bundler like Vite or Webpack.

You can use [this example](https://github.com/saltyaom/elysia-fullstack-example) to quickly try it out.

Otherwise, install it manually:

1. Install Elysia Static plugin

```ts
import { Elysia } from 'elysia'
import { staticPlugin } from '@elysia/static'

new Elysia()
	.use(await staticPlugin()) // [!code ++]
	.listen(3000)
```

:::tip
Notice that we need to add `await` before `staticPlugin()` to enable Fullstack Dev Server.

This is required to setup the necessary HMR hooks.
:::

2. Create **public/index.html** and **index.tsx**

::: code-group

```html [public/index.html]
<!doctype html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Elysia React App</title>

		<meta name="viewport" content="width=device-width, initial-scale=1.0">
	</head>
	<body>
		<div id="root"></div>
		<script type="module" src="./index.tsx"></script>
	</body>
</html>
```

```tsx [public/index.tsx]
import { useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
	const [count, setCount] = useState(0)
	const increase = () => setCount((c) => c + 1)

	return (
		<main>
			<h2>{count}</h2>
			<button onClick={increase}>
				Increase
			</button>
		</main>
	)
}

const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

:::

3. Enable JSX in tsconfig.json

```json
{
  "compilerOptions": {
	"jsx": "react-jsx" // [!code ++]
  }
}
```

4. Navigate to `http://localhost:3000/public` and see the result.

This allows us to develop frontend and backend in a single project without any bundler.

We have verified that Fullstack Dev Server works with HMR, [Tailwind](#tailwind), Tanstack Query, [Eden Treaty](/eden/overview), and path alias.

## Custom prefix path

We can change the default `/public` prefix by passing the `prefix` option to `staticPlugin`.

```ts
import { Elysia } from 'elysia'
import { staticPlugin } from '@elysia/static'

new Elysia()
  	.use(
  		await staticPlugin({
  			prefix: '/' // [!code ++]
   		})
   )
  .listen(3000)
```

This would serve the static files at `/` instead of `/public`.

See [static plugin](/plugins/static) for more configuration options.

## Tailwind CSS

We can also use Tailwind CSS with Bun Fullstack Dev Server.

1. Install dependencies

```bash
bun add tailwindcss@4
bun add -d bun-plugin-tailwind
```

2. Create `bunfig.toml` with the following content:

```toml
[serve.static]
plugins = ["bun-plugin-tailwind"]
```

3. Create a CSS file with Tailwind directives

::: code-group

```css [public/global.css]
@tailwind base;
```

:::

4. Add Tailwind to your HTML or alternatively JavaScript/TypeScript file

::: code-group

```html [public/index.html]
<!doctype html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Elysia React App</title>

		<meta name="viewport" content="width=device-width, initial-scale=1.0">
  		<link rel="stylesheet" href="tailwindcss"> <!-- [!code ++] -->
	</head>
	<body>
		<div id="root"></div>
		<script type="module" src="./index.tsx"></script>
	</body>
</html>
```

```tsx [public/index.tsx]
import { useState } from 'react'
import { createRoot } from 'react-dom/client'

import './global.css' // [!code ++]

function App() {
	const [count, setCount] = useState(0)
	const increase = () => setCount((c) => c + 1)

	return (
		<main>
			<h2>{count}</h2>
			<button onClick={increase}>
				Increase
			</button>
		</main>
	)
}

const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

:::

## Path Alias

We can also use path alias in Bun Fullstack Dev Server.

1. Add `paths` in `tsconfig.json`

```json
{
  "compilerOptions": {
	"baseUrl": ".", // [!code ++]
	"paths": { // [!code ++]
	  "@public/*": ["public/*"] // [!code ++]
	} // [!code ++]
  }
}
```

2. Use the alias in your code

```tsx
import { useState } from 'react'
import { createRoot } from 'react-dom/client'

import '@public/global.css' // [!code ++]

function App() {
	const [count, setCount] = useState(0)
	const increase = () => setCount((c) => c + 1)

	return (
		<main>
			<h2>{count}</h2>
			<button onClick={increase}>
				Increase
			</button>
		</main>
	)
}

const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

This will work out of the box without any additional configuration.

## Build for Production

You can build fullstack server as if it's a normal Elysia server.

```bash
bun build --compile --target bun --outfile server src/index.ts
```

This would create a single executable file **server**.

When running the **server** executable, make sure to include the **public** folder in similar to the development environment.

See [Deploy to Production](/patterns/deploy) for more information.

---

---
url: 'https://elysiajs.com/plugins/graphql-yoga.md'
---

# GraphQL Yoga Plugin

This plugin integrates GraphQL yoga with Elysia

Install with:

```bash
bun add @elysia/graphql-yoga
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { yoga } from '@elysia/graphql-yoga'

const app = new Elysia()
	.use(
		yoga({
			typeDefs: /* GraphQL */ `
				type Query {
					hi: String
				}
			`,
			resolvers: {
				Query: {
					hi: () => 'Hello from Elysia'
				}
			}
		})
	)
	.listen(3000)
```

Accessing `/graphql` in the browser (GET request) would show you a GraphiQL instance for the GraphQL-enabled Elysia server.

Optionally, you can install a custom version of optional peer dependencies as well:

```bash
bun add graphql graphql-yoga
```

## Resolver

Elysia uses [Mobius](https://github.com/saltyaom/mobius) to infer type from **typeDefs** field automatically, allowing you to get full type-safety and auto-complete when typing **resolver** types.

## Context

You can add custom context to the resolver function by adding **context**

```ts
import { Elysia } from 'elysia'
import { yoga } from '@elysia/graphql-yoga'

const app = new Elysia()
	.use(
		yoga({
			typeDefs: /* GraphQL */ `
				type Query {
					hi: String
				}
			`,
			context: {
				name: 'Mobius'
			},
			// If context is a function on this doesn't present
			// for some reason it won't infer context type
			useContext(_) {},
			resolvers: {
				Query: {
					hi: async (parent, args, context) => context.name
				}
			}
		})
	)
	.listen(3000)
```

## Config

This plugin extends [GraphQL Yoga's createYoga options, please refer to the GraphQL Yoga documentation](https://the-guild.dev/graphql/yoga-server/docs) with inlining `schema` config to root.

Below is a config which is accepted by the plugin

### path

@default `/graphql`

Endpoint to expose GraphQL handler

---

---
url: 'https://elysiajs.com/tutorial/getting-started/guard.md'
---

# Guard

When you need to apply multiple hooks to your application, instead of repeating hooks multiple times, you can use `guard` to bulk add hooks to your application.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.onBeforeHandle(({ query: { name }, status }) => { // [!code --]
		if(!name) return status(401) // [!code --]
	}) // [!code --]
	.onBeforeHandle(({ query: { name } }) => { // [!code --]
		console.log(name) // [!code --]
	}) // [!code --]
	.onAfterResponse(({ responseValue }) => { // [!code --]
		console.log(responseValue) // [!code --]
	}) // [!code --]
	.guard({ // [!code ++]
		beforeHandle: [ // [!code ++]
			({ query: { name }, status }) => { // [!code ++]
				if(!name) return status(401) // [!code ++]
			}, // [!code ++]
			({ query: { name } }) => { // [!code ++]
				console.log(name) // [!code ++]
			} // [!code ++]
		], // [!code ++]
		afterResponse({ responseValue }) { // [!code ++]
			console.log(responseValue) // [!code ++]
		} // [!code ++]
	}) // [!code ++]
	.get(
		'/auth',
		({ query: { name = 'anon' } }) => `Hello ${name}!`,
		{
			query: t.Object({
				name: t.String()
			})
		}
	)
	.get(
		'/profile',
		({ query: { name = 'anon' } }) => `Hello ${name}!`,
		{
			query: t.Object({
				name: t.String()
			})
		}
	)
	.listen(3000)
```

Not only that, you can also apply **schema** to multiple routes using `guard`.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.guard({
		beforeHandle: [
			({ query: { name }, status }) => {
				if(!name) return status(401)
			},
			({ query: { name } }) => {
				console.log(name)
			}
		],
		afterResponse({ responseValue }) {
			console.log(responseValue)
		},
		query: t.Object({ // [!code ++]
			name: t.String() // [!code ++]
		}) // [!code ++]
	})
	.get(
		'/auth',
		({ query: { name = 'anon' } }) => `Hello ${name}!`,
		{ // [!code --]
			query: t.Object({ // [!code --]
				name: t.String() // [!code --]
			}) // [!code --]
		} // [!code --]
	)
	.get(
		'/profile',
		({ query: { name = 'anon' } }) => `Hello ${name}!`,
		{ // [!code --]
			query: t.Object({ // [!code --]
				name: t.String() // [!code --]
			}) // [!code --]
		} // [!code --]
	)
	.listen(3000)
```

This will apply hooks and schema to every route **after .guard** is called in the same instance.

See Guard for more information.

## Assignment

Let's put 2 types of hooks into practice.

\<template #answer>

We can use `beforeHandle` to intercept the request before it reaches the handler, and return a response with `status` method.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onBeforeHandle(({ query: { name }, status }) => {
		if(!name) return status(401)
	})
	.get('/auth', ({ query: { name = 'anon' } }) => {
		return `Hello ${name}!`
	})
	.get('/profile', ({ query: { name = 'anon' } }) => {
		return `Hello ${name}!`
	})
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/essential/handler.md'
---

# Handler&#x20;

**Handler** - a function that accepts an HTTP request and returns a response.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    // the function `() => 'hello world'` is a handler
    .get('/', () => 'hello world')
    .listen(3000)
```

A handler may be a literal value, and can be inlined.

```typescript
import { Elysia, file } from 'elysia'

new Elysia()
    .get('/', 'Hello Elysia')
    .get('/video', file('kyuukurarin.mp4'))
    .listen(3000)
```

Using an **inline value** always returns the same value which is useful to optimize performance for static resources like files.

This allows Elysia to compile the response ahead of time to optimize performance.

::: tip
Providing an inline value is not a cache.

Static resource values, headers and status can be mutated dynamically using lifecycle.
:::

## Context

**Context** contains request information which is unique for each request, and is not shared except for `store` (global mutable state).

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', (context) => context.path)
            // ^ This is a context
```

**Context** can only be retrieved in a route handler. It consists of:

#### Property

* [**body**](/essential/validation.html#body) - [HTTP message](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages), form or file upload.
* [**query**](/essential/validation.html#query) - [Query String](https://en.wikipedia.org/wiki/Query_string), includes additional parameters for search query as JavaScript Object. (Query is extracted from a value after pathname starting from '?' question mark sign)
* [**params**](/essential/validation.html#params) - Elysia's path parameters parsed as JavaScript object
* [**headers**](/essential/validation.html#headers) - [HTTP Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers), additional information about the request like User-Agent, Content-Type, Cache Hint.
* [**cookie**](#cookie) - A global mutable signal store for interacting with Cookie (including get/set)
* [**store**](#state) - A global mutable store for Elysia instance

#### Utility Function

* [**redirect**](#redirect) - A function to redirect a response
* [**status**](#status) - A function to return custom status code
* [**set**](#set) - Property to apply to Response:
  * [**headers**](#set.headers) - Response headers

#### Additional Property

* [**request**](#request) - [Web Standard Request](https://developer.mozilla.org/en-US/docs/Web/API/Request)
* [**server**](#server-bun-only) - Bun server instance
* **path** - Pathname of the request

## status&#x20;

A function to return a custom status code with type narrowing.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ status }) => status(418, "Kirifuji Nagisa"))
    .listen(3000)
```

It's recommended to use the **never-throw** approach to return **status** instead of throwing as it:

* allows TypeScript to check if a return value is correctly typed to the response schema
* autocompletion for type narrowing based on status code
* type narrowing for error handling using End-to-end type safety ([Eden](/eden/overview))

## Set

**set** is a mutable property that forms a response accessible via `Context.set`.

```ts
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ set, status }) => {
		set.headers = { 'X-Teapot': 'true' }

		return status(418, 'I am a teapot')
	})
	.listen(3000)
```

### set.headers

Allows us to append or delete response headers represented as an Object.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ set }) => {
        set.headers['x-powered-by'] = 'Elysia'

        return 'a mimir'
    })
    .listen(3000)
```

::: tip
Elysia provides auto-completion for lowercase for case-sensitivity consistency, eg. use `set-cookie` rather than `Set-Cookie`.
:::

Redirect a request to another resource.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ redirect }) => {
        return redirect('https://youtu.be/whpVWVWBW4U?&t=8')
    })
    .get('/custom-status', ({ redirect }) => {
        // You can also set custom status to redirect
        return redirect('https://youtu.be/whpVWVWBW4U?&t=8', 302)
    })
    .listen(3000)
```

When using redirect, returned value is not required and will be ignored. As response will be from another resource.

Set a default status code if not provided.

It's recommended to use this in a plugin that only needs to return a specific status code while allowing the user to return a custom value. For example, HTTP 201/206 or 403/405, etc.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onBeforeHandle(({ set }) => {
        set.status = 418

        return 'Kirifuji Nagisa'
    })
    .get('/', () => 'hi')
    .listen(3000)
```

Unlike the `status` function, `set.status` cannot infer the return value type, therefore it can't check if the return value is correctly typed to the response schema.

::: tip
HTTP Status indicates the type of response. If the route handler is executed successfully without error, Elysia will return the status code 200.
:::

You can also set a status code using the common name of the status code instead of using a number.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ set }) => {
        set.status = 418

        return 'Kirifuji Nagisa'
    })
    .listen(3000)
```

## Cookie

Elysia provides a mutable store for interacting with cookies.

There's no need for get/set; you can extract the cookie name and retrieve or update its value directly.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/set', ({ cookie: { name } }) => {
		// Get
        name.value

        // Set
        name.value = "New Value"
	})
```

See [Patterns: Cookie](/patterns/cookie) for more information.

## Redirect

Redirect a request to another resource.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ redirect }) => {
		return redirect('https://youtu.be/whpVWVWBW4U?&t=8')
	})
	.get('/custom-status', ({ redirect }) => {
		// You can also set custom status to redirect
		return redirect('https://youtu.be/whpVWVWBW4U?&t=8', 302)
	})
	.listen(3000)
```

When using redirect, returned value is not required and will be ignored. As response will be from another resource.

## Formdata

We can return a `FormData` by returning the `form` utility directly from the handler.

```typescript
import { Elysia, form, file } from 'elysia'

new Elysia()
	.get('/', () => form({
		name: 'Tea Party',
		images: [file('nagi.web'), file('mika.webp')]
	}))
	.listen(3000)
```

This pattern is useful if you ever need to return a file or multipart form data.

### Return a file

Or alternatively, you can return a single file by returning `file` directly without `form`.

```typescript
import { Elysia, file } from 'elysia'

new Elysia()
	.get('/', file('nagi.web'))
	.listen(3000)
```

## Stream

To return a response streaming out of the box, use a generator function with the `yield` keyword.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/ok', function* () {
		yield 1
		yield 2
		yield 3
	})
```

In this example, we stream a response by using the `yield` keyword.

## Server Sent Events (SSE)

Elysia supports [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) by providing a `sse` utility function.

```typescript
import { Elysia, sse } from 'elysia'

new Elysia()
	.get('/sse', function* () {
		yield sse('hello world')
		yield sse({
			event: 'message',
			data: {
				message: 'This is a message',
				timestamp: new Date().toISOString()
			},
		})
	})
```

When a value is wrapped in `sse`, Elysia will automatically set the response headers to `text/event-stream` and format the data as an SSE event.

### Headers in Server-Sent Event

Headers can only be set before the first chunk is yielded.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/ok', function* ({ set }) {
		// This will set headers
		set.headers['x-name'] = 'Elysia'
		yield 1
		yield 2

		// This will do nothing
		set.headers['x-id'] = '1'
		yield 3
	})
```

Once the first chunk is yielded, Elysia will send the headers to the client, therefore mutating headers after the first chunk is yielded will do nothing.

### Conditional Stream

If the response is returned without yield, Elysia will automatically convert stream to normal response instead.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/ok', function* () {
		if (Math.random() > 0.5) return 'ok'

		yield 1
		yield 2
		yield 3
	})
```

This allows us to conditionally stream a response or return a normal response if necessary.

### Automatic cancellation

Before response streaming is completed, if the user cancels the request, Elysia will automatically stop the generator function.

### Eden

[Eden](/eden/overview) will interpret a stream response as `AsyncGenerator` allowing us to use `for await` loop to consume the stream.

```typescript
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia()
	.get('/ok', function* () {
		yield 1
		yield 2
		yield 3
	})

const { data, error } = await treaty(app).ok.get()
if (error) throw error

for await (const chunk of data)
	console.log(chunk)
```

## Request

Elysia is built on top of [Web Standard Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) which is shared between multiple runtime like Node, Bun, Deno, Cloudflare Worker, Vercel Edge Function, and more.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/user-agent', ({ request }) => {
		return request.headers.get('user-agent')
	})
	.listen(3000)
```

This allows access to low-level request information if necessary.

## Server Bun only

Server instance is a Bun server instance, allowing us to access server information like port number or request IP.

Server will only be available when HTTP server is running with `listen`.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/port', ({ server }) => {
		return server?.port
	})
	.listen(3000)
```

### Request IP Bun only

We can get request IP by using `server.requestIP` method

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/ip', ({ server, request }) => {
		return server?.requestIP(request)
	})
	.listen(3000)
```

## Extending context Advanced concept

Elysia provides a minimal Context by default, allowing you to extend the Context for your specific needs using state, decorate, derive, and resolve.

See [Extends Context](/patterns/extends-context) for more information on how to extend a Context.

---

---
url: 'https://elysiajs.com/tutorial/getting-started/handler-and-context.md'
---

# Handler and Context

**Handler** - a resource or a route function to send data back to client.

```ts
import { Elysia } from 'elysia'

new Elysia()
    // `() => 'hello world'` is a handler
    .get('/', () => 'hello world')
    .listen(3000)
```

A handler can also be a literal value, see Handler

```ts
import { Elysia } from 'elysia'

new Elysia()
    // `'hello world'` is a handler
    .get('/', 'hello world')
    .listen(3000)
```

Using an inline value can be useful for static resources like **files**.

## Context

Contains information about each request. It is passed as the only argument of a handler.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', (context) => context.path)
            // ^ This is a context
```

**Context** stores information about the request like:

* body - data sent by client to server like form data, JSON payload.
* query - query string as an object. (Query is extracted from a value after pathname starting from '?' question mark sign)
* params - Path parameters parsed as object
* headers - HTTP Header, additional information about the request like "Content-Type".

See Context.

## Preview

You can preview the result by looking under the **editor** section.

There should be a tiny navigator on the **top left** of the preview window.

You can use it to switch between path and method to see the response.

You can also click  to edit body, and headers.

## Assignment

Let's try extracting context parameters:

\<template #answer>

1. We can extract `body`, `query`, and `headers` from the first parameter of a callback function.
2. We can then return them like `{ body, query, headers }`.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.post('/', ({ body, query, headers }) => {
		return {
			query,
			body,
			headers
		}
	})
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/plugins/html.md'
---

# HTML Plugin

Allows you to use [JSX](#jsx) and HTML with proper headers and support.

Install with:

```bash
bun add @elysia/html
```

Then use it:

```tsx twoslash
import React from 'react'
// ---cut---
import { Elysia } from 'elysia'
import { html, Html } from '@elysia/html'

new Elysia()
	.use(html())
	.get(
		'/html',
		() => `
            <html lang='en'>
                <head>
                    <title>Hello World</title>
                </head>
                <body>
                    <h1>Hello World</h1>
                </body>
            </html>`
	)
	.get('/jsx', () => (
		<html lang="en">
			<head>
				<title>Hello World</title>
			</head>
			<body>
				<h1>Hello World</h1>
			</body>
		</html>
	))
	.listen(3000)
```

This plugin will automatically add `Content-Type: text/html; charset=utf8` header to the response, add `<!doctype html>`, and convert it into a Response object.

## JSX

Elysia HTML is based on [@kitajs/html](https://github.com/kitajs/html) allowing us to define JSX to string in compile time to achieve high performance.

Name your file that needs to use JSX to end with affix **"x"**:

* .js -> .jsx
* .ts -> .tsx

To register the TypeScript type, please append the following to **tsconfig.json**:

```jsonc
// tsconfig.json
{
	"compilerOptions": {
		"jsx": "react",
		"jsxFactory": "Html.createElement",
		"jsxFragmentFactory": "Html.Fragment"
	}
}
```

That's it, now you can use JSX as your template engine:

```tsx twoslash
import React from 'react'
// ---cut---
import { Elysia } from 'elysia'
import { html, Html } from '@elysia/html' // [!code ++]

new Elysia()
	.use(html()) // [!code ++]
	.get('/', () => (
		<html lang="en">
			<head>
				<title>Hello World</title>
			</head>
			<body>
				<h1>Hello World</h1>
			</body>
		</html>
	))
	.listen(3000)
```

If the error `Cannot find name 'Html'. Did you mean 'html'?` occurs, this import must be added to the JSX template:

```tsx
import { Html } from '@elysia/html'
```

It is important that it is written in uppercase.

## XSS

Elysia HTML is based use of the Kita HTML plugin to detect possible XSS attacks in compile time.

You can use a dedicated `safe` attribute to sanitize user value to prevent XSS vulnerability.

```tsx
import { Elysia, t } from 'elysia'
import { html, Html } from '@elysia/html'

new Elysia()
	.use(html())
	.post(
		'/',
		({ body }) => (
			<html lang="en">
				<head>
					<title>Hello World</title>
				</head>
				<body>
					<h1 safe>{body}</h1>
				</body>
			</html>
		),
		{
			body: t.String()
		}
	)
	.listen(3000)
```

However, when building a large-scale app, it's best to have a type reminder to detect possible XSS vulnerabilities in your codebase.

To add a type-safe reminder, please install:

```sh
bun add @kitajs/ts-html-plugin
```

Then appends the following **tsconfig.json**

```jsonc
// tsconfig.json
{
	"compilerOptions": {
		"jsx": "react",
		"jsxFactory": "Html.createElement",
		"jsxFragmentFactory": "Html.Fragment",
		"plugins": [{ "name": "@kitajs/ts-html-plugin" }]
	}
}
```

## Options

### contentType

* Type: `string`
* Default: `'text/html; charset=utf8'`

The content-type of the response.

### autoDetect

* Type: `boolean`
* Default: `true`

Whether to automatically detect HTML content and set the content-type.

### autoDoctype

* Type: `boolean | 'full'`
* Default: `true`

Whether to automatically add `<!doctype html>` to a response starting with `<html>`, if not found.

Use `full` to also automatically add doctypes on responses returned without this plugin

```ts
// without the plugin
app.get('/', () => '<html></html>')

// With the plugin
app.get('/', ({ html }) => html('<html></html>'))
```

### isHtml

* Type: `(value: string) => boolean`
* Default: `isHtml` (exported function)

The function is used to detect if a string is HTML or not. Default implementation if length is greater than 7, starts with `<` and ends with `>`.

Keep in mind there's no real way to validate HTML, so the default implementation is a best guess.

---

---
url: 'https://elysiajs.com/integrations/ai-sdk.md'
---

# Integration with AI SDK

Elysia provides support for response streaming with ease, allowing you to integrate with [Vercel AI SDKs](https://vercel.com/docs/ai) seamlessly.

## Response Streaming

Elysia supports continuous streaming of a `ReadableStream` and `Response`, allowing you to return streams directly from the AI SDKs.

```ts
import { Elysia } from 'elysia'
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'

new Elysia().get('/', () => {
    const stream = streamText({
        model: openai('gpt-5'),
        system: 'You are Yae Miko from Genshin Impact',
        prompt: 'Hi! How are you doing?'
    })

    // Just return a ReadableStream
    return stream.textStream // [!code ++]

    // UI Message Stream is also supported
    return stream.toUIMessageStream() // [!code ++]
})
```

Elysia will handle the stream automatically, allowing you to use it in various ways.

## Server-Sent Events

Elysia also supports Server-Sent Events for streaming responses by simply wrapping a `ReadableStream` with the `sse` function.

```ts
import { Elysia, sse } from 'elysia' // [!code ++]
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'

new Elysia().get('/', () => {
    const stream = streamText({
        model: openai('gpt-5'),
        system: 'You are Yae Miko from Genshin Impact',
        prompt: 'Hi! How are you doing?'
    })

    // Each chunk will be sent as a Server Sent Event
    return sse(stream.textStream) // [!code ++]

    // UI Message Stream is also supported
    return sse(stream.toUIMessageStream()) // [!code ++]
})
```

## As Response

If you don't need type safety from the stream for further usage with [Eden](/eden/overview), you can return the stream directly as a response.

```ts
import { Elysia } from 'elysia'
import { ai } from 'ai'
import { openai } from '@ai-sdk/openai'

new Elysia().get('/', () => {
    const stream = streamText({
        model: openai('gpt-5'),
        system: 'You are Yae Miko from Genshin Impact',
        prompt: 'Hi! How are you doing?'
    })

    return stream.toTextStreamResponse() // [!code ++]

    // UI Message Stream Response will use SSE
    return stream.toUIMessageStreamResponse() // [!code ++]
})
```

## Manual Streaming

If you want to have more control over the streaming, you can use a generator function to yield the chunks manually.

```ts
import { Elysia, sse } from 'elysia'
import { ai } from 'ai'
import { openai } from '@ai-sdk/openai'

new Elysia().get('/', async function* () {
    const stream = streamText({
        model: openai('gpt-5'),
        system: 'You are Yae Miko from Genshin Impact',
        prompt: 'Hi! How are you doing?'
    })

    for await (const data of stream.textStream) // [!code ++]
        yield sse({ // [!code ++]
            data, // [!code ++]
            event: 'message' // [!code ++]
        }) // [!code ++]

    yield sse({
        event: 'done'
    })
})
```

## Fetch

If the AI SDK doesn't support the model you're using, you can still use the `fetch` function to make requests to the AI SDKs and stream the response directly.

```ts
import { Elysia, fetch } from 'elysia'

new Elysia().get('/', () => {
    return fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${process.env.OPENAI_API_KEY}`
        },
        body: JSON.stringify({
            model: 'gpt-5',
            stream: true,
            messages: [
                {
                    role: 'system',
                    content: 'You are Yae Miko from Genshin Impact'
                },
                { role: 'user', content: 'Hi! How are you doing?' }
            ]
        })
    })
})
```

Elysia will proxy the fetch response with streaming support automatically.

***

For additional information, please refer to the [AI SDK documentation](https://ai-sdk.dev/docs/introduction)

---

---
url: 'https://elysiajs.com/integrations/astro.md'
---

# Integration with Astro

With [Astro Endpoint](https://docs.astro.build/en/core-concepts/endpoints/), we can run Elysia on Astro directly.

1. Set **output** to **server** in **astro.config.mjs**

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config'

// https://astro.build/config
export default defineConfig({
    output: 'server' // [!code ++]
})
```

2. Create **pages/\[...slugs].ts**
3. Create or import an existing Elysia server in **\[...slugs].ts**
4. Export the handler with the name of the method you want to expose

```typescript
// pages/[...slugs].ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/api', () => 'hi')
    .post('/api', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

const handle = ({ request }: { request: Request }) => app.handle(request) // [!code ++]

export const GET = handle // [!code ++]
export const POST = handle // [!code ++]
```

Elysia will work normally as expected because of WinterTC compliance.

We recommend running [Astro on Bun](https://docs.astro.build/en/recipes/bun) as Elysia is designed to be run on Bun.

::: tip
You can run Elysia server without running Astro on Bun thanks to WinterTC support.
:::

With this approach, you can have co-location of both frontend and backend in a single repository and have End-to-end type-safety with Eden.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Prefix

If you place an Elysia server not in the root directory of the app router, you need to annotate the prefix on the Elysia server.

For example, if you place the Elysia server in **pages/api/\[...slugs].ts**, you need to annotate the prefix as **/api** on the Elysia server.

```typescript
// pages/api/[...slugs].ts
import { Elysia, t } from 'elysia'

const app = new Elysia({ prefix: '/api' }) // [!code ++]
    .get('/', () => 'hi')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

const handle = ({ request }: { request: Request }) => app.handle(request) // [!code ++]

export const GET = handle // [!code ++]
export const POST = handle // [!code ++]
```

This will ensure that Elysia routing works properly wherever you place it.

Please refer to [Astro Endpoints](https://docs.astro.build/en/core-concepts/endpoints/) for more information.

---

---
url: 'https://elysiajs.com/integrations/cloudflare-worker.md'
---

# Cloudflare Worker Experimental

Elysia now supports Cloudflare Worker with an **experimental** Cloudflare Worker Adapter.

1. You will need [Wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update) to setup, and start a development server.

```bash
wrangler init elysia-on-cloudflare
```

2. Then add Cloudflare Adapter to your Elysia app, and make sure to call `.compile()` before exporting the app.

```ts
import { Elysia } from 'elysia'
import { CloudflareAdapter } from 'elysia/adapter/cloudflare-worker' // [!code ++]

export default new Elysia({
	adapter: CloudflareAdapter // [!code ++]
})
	.get('/', () => 'Hello Cloudflare Worker!')
	// This is required to make Elysia work on Cloudflare Worker
	.compile() // [!code ++]
```

3. Make sure to have `compatibility_date` set to at least `2025-06-01` in your wrangler config

::: code-group

```jsonc [wrangler.jsonc]
{
	"$schema": "node_modules/wrangler/config-schema.json",
 	"name": "elysia-on-cloudflare",
	"main": "src/index.ts",
	"compatibility_date": "2025-06-01" // [!code ++]
}
```

```toml [wrangler.toml]
main = "src/index.ts"
name = "elysia-on-cloudflare"
compatibility_date = "2025-06-01" # [!code ++]
```

:::

4. Now you can start the development server with:

```bash
wrangler dev
```

This should start a development server at `http://localhost:8787`

You don't need a `nodejs_compat` flag as Elysia doesn't use any Node.js built-in modules (or the ones we use don't support Cloudflare Worker yet).

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Limitations

Here are some known limitations of using Elysia on Cloudflare Workers:

1. `Elysia.file`, and [Static Plugin](/plugins/static) don't work [due to the lack of the `fs` module](https://developers.cloudflare.com/workers/runtime-apis/nodejs/#supported-nodejs-apis); see the [Static File](#static-file) section for alternatives
2. [OpenAPI Type Gen](/blog/openapi-type-gen) doesn't work [due to the lack of the `fs` module](https://developers.cloudflare.com/workers/runtime-apis/nodejs/#supported-nodejs-apis)
3. You can't define [**Response** before server start](https://x.com/saltyAom/status/1966602691754553832) or use a plugin that does so
4. You can't inline a value due to #3.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	// This will throw error
    .get('/', 'Hello Elysia')
    .listen(3000)
```

## Static Files

[Static Plugin](/plugins/static) doesn't work, but you can still serve static files with [Cloudflare's built-in static file serving](https://developers.cloudflare.com/workers/static-assets/).

Add the following to your wrangler config:

::: code-group

```jsonc [wrangler.jsonc]
{
	"$schema": "node_modules/wrangler/config-schema.json",
 	"name": "elysia-on-cloudflare",
	"main": "src/index.ts",
	"compatibility_date": "2025-06-01",
	"assets": { "directory": "public" } // [!code ++]
}
```

```toml [wrangler.toml]
name = "elysia-on-cloudflare"
main = "src/index.ts"
compatibility_date = "2025-06-01"
assets = { directory = "public" } # [!code ++]
```

:::

Create a `public` folder and place your static files in it.

For example, if you have a folder structure like this:

```
│
├─ public
│  ├─ kyuukurarin.mp4
│  └─ static
│     └─ mika.webp
├─ src
│  └── index.ts
└─ wrangler.toml
```

Then you should be able to access your static files from the following paths:

* **http://localhost:8787/kyuukurarin.mp4**
* **http://localhost:8787/static/mika.webp**

## Bindings

You can use Cloudflare Workers bindings by importing env from `cloudflare:workers`.

```ts
import { Elysia } from 'elysia'
import { CloudflareAdapter } from 'elysia/adapter/cloudflare-worker'
import { env } from 'cloudflare:workers' // [!code ++]

export default new Elysia({
	adapter: CloudflareAdapter
})
	.get('/', () => `Hello ${await env.KV.get('my-key')}`) // [!code ++]
	.compile()
```

See [Cloudflare Workers: Bindings](https://developers.cloudflare.com/workers/runtime-apis/bindings/#importing-env-as-a-global) for more information about bindings.

## AoT compilation

Previously, to use Elysia on Cloudflare Worker, you have to pass `aot: false` to the Elysia constructor.

This is no longer necessary as [Cloudflare now supports Function compilation during startup](https://developers.cloudflare.com/workers/configuration/compatibility-flags/#enable-eval-during-startup).

As of Elysia 1.4.7, you can now use Ahead of Time Compilation with Cloudflare Worker, and drop the `aot: false` flag.

```ts
import { Elysia } from 'elysia'
import { CloudflareAdapter } from 'elysia/adapter/cloudflare-worker' // [!code ++]

export default new Elysia({
	aot: false, // [!code --]
	adapter: CloudflareAdapter // [!code ++]
})
```

Otherwise, you can still use `aot: false` if you don't want Ahead of Time Compilation, but we recommend using it for better performance and accurate plugin encapsulation.

---

---
url: 'https://elysiajs.com/integrations/deno.md'
---

# Integration with Deno

Elysia is built on top of Web Standard Request/Response, allowing us to run Elysia with Deno.serve directly.

To run Elysia on Deno, wrap `Elysia.fetch` in `Deno.serve`

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', () => 'Hello Elysia')
	.listen(3000) // [!code --]

Deno.serve(app.fetch) // [!code ++]
```

Then you can run the server with `deno serve`:

```bash
deno serve --watch src/index.ts
```

This is all you need to run Elysia on Deno.

### Change Port Number

You can specify the port number in `Deno.serve`.

```ts
Deno.serve(app.fetch) // [!code --]
Deno.serve({ port:8787 }, app.fetch) // [!code ++]
```

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

---

---
url: 'https://elysiajs.com/integrations/drizzle.md'
---

# Drizzle

Drizzle ORM is a headless TypeScript ORM with a focus on type safety and developer experience.

We may convert Drizzle schema to Elysia validation models using `drizzle-typebox`

### Drizzle Typebox

[Elysia.t](/essential/validation.html#elysia-type) is a fork of TypeBox, allowing us to use any TypeBox type in Elysia directly.

We can convert Drizzle schema into TypeBox schema using ["drizzle-typebox"](https://npmjs.org/package/drizzle-typebox), and use it directly on Elysia's schema validation.

### Here's how it works:

1. Define your database schema in Drizzle.
2. Convert Drizzle schema into Elysia validation models using `drizzle-typebox`.
3. Use the converted Elysia validation models to ensure type validation.
4. OpenAPI schema is generated from Elysia validation models.
5. Add [Eden Treaty](/eden/overview) to add type-safety to your frontend.

```
                                                    * ——————————————— *
                                                    |                 |
                                               | -> |  Documentation  |
* ————————— *             * ———————— * OpenAPI |    |                 |
|           |   drizzle-  |          | ——————— |    * ——————————————— *
|  Drizzle  | —————————-> |  Elysia  |
|           |  -typebox   |          | ——————— |    * ——————————————— *
* ————————— *             * ———————— *   Eden  |    |                 |
                                               | -> |  Frontend Code  |
												    |                 |
												    * ——————————————— *

```

## Installation

To install Drizzle, run the following command:

```bash
bun add drizzle-orm drizzle-typebox
```

Then you need to pin `@sinclair/typebox` as there might be a mismatch version between `drizzle-typebox` and `Elysia`, this may cause conflict of Symbols between two versions.

We recommend pinning the version of `@sinclair/typebox` to the **minimum version** used by `elysia` by using:

```bash
grep "@sinclair/typebox" node_modules/elysia/package.json
```

We may use `overrides` field in `package.json` to pin the version of `@sinclair/typebox`:

```json
{
  "overrides": {
  	"@sinclair/typebox": "0.32.4"
  }
}
```

## Drizzle schema

Assuming we have a `user` table in our codebase as follows:

::: code-group

```ts [src/database/schema.ts]
import {
    pgTable,
    varchar,
    timestamp
} from 'drizzle-orm/pg-core'

import { createId } from '@paralleldrive/cuid2'

export const user = pgTable(
    'user',
    {
        id: varchar('id')
            .$defaultFn(() => createId())
            .primaryKey(),
        username: varchar('username').notNull().unique(),
        password: varchar('password').notNull(),
        email: varchar('email').notNull().unique(),
        salt: varchar('salt', { length: 64 }).notNull(),
        createdAt: timestamp('created_at').defaultNow().notNull(),
    }
)

export const table = {
	user
} as const

export type Table = typeof table
```

:::

## drizzle-typebox

We may convert the `user` table into TypeBox models by using `drizzle-typebox`:

::: code-group

```ts [src/index.ts]
import { t } from 'elysia'
import { createInsertSchema } from 'drizzle-typebox'
import { table } from './database/schema'

const _createUser = createInsertSchema(table.user, {
	// Replace email with Elysia's email type
	email: t.String({ format: 'email' })
})

new Elysia()
	.post('/sign-up', ({ body }) => {
		// Create a new user
	}, {
		body: t.Omit(
			_createUser,
			['id', 'salt', 'createdAt']
		)
	})
```

:::

This allows us to reuse the database schema in Elysia validation models

## Type instantiation is possibly infinite

If you got an error like **Type instantiation is possibly infinite** this is because of the circular reference between `drizzle-typebox` and `Elysia`.

If we nested a type from drizzle-typebox into Elysia schema, it will cause an infinite loop of type instantiation.

To prevent this, we need to **explicitly define a type between `drizzle-typebox` and `Elysia`** schema:

```ts
import { t } from 'elysia'
import { createInsertSchema } from 'drizzle-typebox'

import { table } from './database/schema'

const _createUser = createInsertSchema(table.user, {
	email: t.String({ format: 'email' })
})

// ✅ This works, by referencing the type from `drizzle-typebox`
const createUser = t.Omit(
	_createUser,
	['id', 'salt', 'createdAt']
)

// ❌ This will cause an infinite loop of type instantiation
const createUser = t.Omit(
	createInsertSchema(table.user, {
		email: t.String({ format: 'email' })
	}),
	['id', 'salt', 'createdAt']
)
```

Always declare a variable for `drizzle-typebox` and reference it if you want to use Elysia type

## Utility

As we are likely going to use `t.Pick` and `t.Omit` to exclude or include certain fields, it may be cumbersome to repeat the process:

We recommend using these utility functions **(copy as-is)** to simplify the process:

::: code-group

```ts [src/database/utils.ts]
/**
 * @lastModified 2025-02-04
 * @see https://elysiajs.com/recipe/drizzle.html#utility
 */

import { Kind, type TObject } from '@sinclair/typebox'
import {
    createInsertSchema,
    createSelectSchema,
    BuildSchema,
} from 'drizzle-typebox'

import { table } from './schema'
import type { Table } from 'drizzle-orm'

type Spread<
    T extends TObject | Table,
    Mode extends 'select' | 'insert' | undefined,
> =
    T extends TObject<infer Fields>
        ? {
              [K in keyof Fields]: Fields[K]
          }
        : T extends Table
          ? Mode extends 'select'
              ? BuildSchema<
                    'select',
                    T['_']['columns'],
                    undefined
                >['properties']
              : Mode extends 'insert'
                ? BuildSchema<
                      'insert',
                      T['_']['columns'],
                      undefined
                  >['properties']
                : {}
          : {}

/**
 * Spread a Drizzle schema into a plain object
 */
export const spread = <
    T extends TObject | Table,
    Mode extends 'select' | 'insert' | undefined,
>(
    schema: T,
    mode?: Mode,
): Spread<T, Mode> => {
    const newSchema: Record<string, unknown> = {}
    let table

    switch (mode) {
        case 'insert':
        case 'select':
            if (Kind in schema) {
                table = schema
                break
            }

            table =
                mode === 'insert'
                    ? createInsertSchema(schema)
                    : createSelectSchema(schema)

            break

        default:
            if (!(Kind in schema)) throw new Error('Expect a schema')
            table = schema
    }

    for (const key of Object.keys(table.properties))
        newSchema[key] = table.properties[key]

    return newSchema as any
}

/**
 * Spread a Drizzle Table into a plain object
 *
 * If `mode` is 'insert', the schema will be refined for insert
 * If `mode` is 'select', the schema will be refined for select
 * If `mode` is undefined, the schema will be spread as is, models will need to be refined manually
 */
export const spreads = <
    T extends Record<string, TObject | Table>,
    Mode extends 'select' | 'insert' | undefined,
>(
    models: T,
    mode?: Mode,
): {
    [K in keyof T]: Spread<T[K], Mode>
} => {
    const newSchema: Record<string, unknown> = {}
    const keys = Object.keys(models)

    for (const key of keys) newSchema[key] = spread(models[key], mode)

    return newSchema as any
}
```

:::

This utility function will convert Drizzle schema into a plain object, which can pick by property name as plain object:

```ts
// ✅ Using spread utility function
const user = spread(table.user, 'insert')

const createUser = t.Object({
	id: user.id, // { type: 'string' }
	username: user.username, // { type: 'string' }
	password: user.password // { type: 'string' }
})

// ⚠️ Using t.Pick
const _createUser = createInsertSchema(table.user)

const createUser = t.Pick(
	_createUser,
	['id', 'username', 'password']
)
```

### Table Singleton

We recommend using a singleton pattern to store the table schema, this will allow us to access the table schema from anywhere in the codebase:

::: code-group

```ts [src/database/model.ts]
import { table } from './schema'
import { spreads } from './utils'

export const db = {
	insert: spreads({
		user: table.user,
	}, 'insert'),
	select: spreads({
		user: table.user,
	}, 'select')
} as const
```

:::

This will allow us to access the table schema from anywhere in the codebase:

::: code-group

```ts [src/index.ts]
import { Elysia, t } from 'elysia'
import { db } from './database/model'

const { user } = db.insert

new Elysia()
	.post('/sign-up', ({ body }) => {
		// Create a new user
	}, {
		body: t.Object({
			id: user.username,
			username: user.username,
			password: user.password
		})
	})
```

:::

### Refinement

If type refinement is needed, you may use `createInsertSchema` and `createSelectSchema` to refine the schema directly.

::: code-group

```ts [src/database/model.ts]
import { t } from 'elysia'
import { createInsertSchema, createSelectSchema } from 'drizzle-typebox'

import { table } from './schema'
import { spreads } from './utils'

export const db = {
	insert: spreads({
		user: createInsertSchema(table.user, {
			email: t.String({ format: 'email' })
		}),
	}, 'insert'),
	select: spreads({
		user: createSelectSchema(table.user, {
			email: t.String({ format: 'email' })
		})
	}, 'select')
} as const
```

:::

In the code above, we refine a `user.email` schema to include a `format` property

The `spread` utility function will skip a refined schema, so you can use it as is.

***

For more information, please refer to the [Drizzle ORM](https://orm.drizzle.team) and [Drizzle TypeBox](https://orm.drizzle.team/docs/typebox) documentation.

---

---
url: 'https://elysiajs.com/integrations/expo.md'
---

# Integration with Expo

Starting from Expo SDK 50, and App Router v3, Expo allows us to create API route directly in an Expo app.

1. Create **app/\[...slugs]+api.ts**
2. Define an Elysia server
3. Export **Elysia.fetch** with the name of the HTTP methods you want to use

::: code-group

```typescript [app/[...slugs]+api.ts]
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/', 'hello Expo')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

export const GET = app.fetch // [!code ++]
export const POST = app.fetch // [!code ++]
```

:::

You can treat the Elysia server as if it were a normal Expo API route.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Prefix

If you place an Elysia server not in the root directory of the app router, you need to annotate the prefix on the Elysia server.

For example, if you place the Elysia server in **app/api/\[...slugs]+api.ts**, you need to annotate the prefix as **/api** on the Elysia server.

::: code-group

```typescript [app/api/[...slugs]+api.ts]
import { Elysia, t } from 'elysia'

const app = new Elysia({ prefix: '/api' }) // [!code ++]
    .get('/', 'Hello Expo')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

export const GET = app.fetch
export const POST = app.fetch
```

:::

This will ensure that Elysia routing works properly wherever you place it.

## Eden

We can add [Eden](/eden/overview) for **end-to-end type safety** similar to tRPC.

1. Export `type` from the Elysia server

::: code-group

```typescript [app/[...slugs]+api.ts]
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', 'Hello Nextjs')
	.post(
		'/user',
		({ body }) => body,
		{
			body: treaty.schema('User', {
				name: 'string'
			})
		}
	)

export type app = typeof app // [!code ++]

export const GET = app.fetch
export const POST = app.fetch
```

:::

2. Create a Treaty client

::: code-group

```typescript [lib/eden.ts]
import { treaty } from '@elysia/eden'
import type { app } from '../app/[...slugs]+api'

export const api = treaty<app>('localhost:3000/api')
```

:::

3. Use the client in both server and client components

::: code-group

```tsx [app/page.tsx]
import { api } from '../lib/eden'

export default async function Page() {
	const message = await api.get()

	return <h1>Hello, {message}</h1>
}
```

:::

## Deployment

You can either directly use the API route with Elysia and deploy as a normal Elysia app if needed, or use the [experimental Expo server runtime](https://docs.expo.dev/router/reference/api-routes/#deployment).

If you are using the Expo server runtime, you may use the `expo export` command to create an optimized build for your Expo app. This will include an Expo function that uses Elysia at **dist/server/\_expo/functions/\[...slugs]+api.js**

::: tip
Please note that Expo Functions are treated as Edge functions instead of normal servers, so running the Edge function directly will not allocate any port.
:::

You may use the Expo function adapter provided by Expo to deploy your Edge Function.

Currently, Expo supports the following adapters:

* [Express](https://docs.expo.dev/router/reference/api-routes/#express)
* [Netlify](https://docs.expo.dev/router/reference/api-routes/#netlify)
* [Vercel](https://docs.expo.dev/router/reference/api-routes/#vercel)

---

---
url: 'https://elysiajs.com/integrations/netlify.md'
---

# Integration with Netlify Edge Function

[Netlify Edge Functions](https://docs.netlify.com/build/edge-functions/overview/) run on [Deno](/integrations/deno), which is one of Elysia's supported runtimes, as Elysia is built on top of Web Standards.

Netlify Edge Functions require a special directory to run a function; the default is **\<directory>/netlify/edge-functions**.

To create a function at **/hello**, you would need to create a file at `netlify/edge-functions/hello.ts`, then simply `export default` an Elysia instance.

::: code-group

```typescript [netlify/edge-functions/hello.ts]
import { Elysia } from 'elysia'

export const config = { path: '/hello' } // [!code ++]

export default new Elysia({ prefix: '/hello' }) // [!code ++]
	.get('/', () => 'Hello Elysia')
```

:::

### Running locally

To test your Elysia server on Netlify Edge Functions locally, you can install the [Netlify CLI](https://docs.netlify.com/build/edge-functions/get-started/#test-locally) to simulate function invocation.

To install Netlify CLI:

```bash
bun add -g netlify-cli
```

To run the development environment:

```bash
netlify dev
```

For additional information, please refer to the [Netlify Edge Functions documentation](https://docs.netlify.com/build/edge-functions).

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

---

---
url: 'https://elysiajs.com/integrations/nextjs.md'
---

# Integration with Next.js

With Next.js App Router, we can run Elysia on Next.js routes.

1. Create **app/api/\[\[...slugs]]/route.ts**
2. Define an Elysia server
3. Export **Elysia.fetch** with the name of the HTTP methods you want to use

::: code-group

```typescript [app/api/[[...slugs]]/route.ts]
import { Elysia, t } from 'elysia'

const app = new Elysia({ prefix: '/api' })
    .get('/', 'Hello Nextjs')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

export const GET = app.fetch // [!code ++]
export const POST = app.fetch // [!code ++]
```

:::

Elysia will work normally because of WinterTC compliance.

You can treat the Elysia server as a normal Next.js API route.

With this approach, you can have co-location of both frontend and backend in a single repository and have [End-to-end type safety with Eden](/eden/overview) with both client-side and server action

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Prefix

Because our Elysia server is not in the root directory of the app router, you need to annotate the prefix on the Elysia server.

For example, if you place the Elysia server in **app/user/\[\[...slugs]]/route.ts**, you need to annotate the prefix as **/user** on the Elysia server.

::: code-group

```typescript [app/user/[[...slugs]]/route.ts]
import { Elysia, t } from 'elysia'

const app = new Elysia({ prefix: '/user' }) // [!code ++]
	.get('/', 'Hello Nextjs')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

export const GET = app.fetch
export const POST = app.fetch
```

:::

This will ensure that Elysia routing works properly wherever you place it.

## Eden

We can add [Eden](/eden/overview) for **end-to-end type safety** similar to tRPC.

In this approach, we will use the isomorphic fetch pattern to allow Elysia to:

1. On Server: directly call Elysia without going through the network layer
2. On Client: call Elysia through the network layer

To start, we need to do the following steps:

1. Export Elysia instance

::: code-group

```typescript [app/api/[[...slugs]]/route.ts]
import { Elysia } from 'elysia'

export const app = new Elysia({ prefix: '/api' }) // [!code ++]
	.get('/', 'Hello Nextjs')
	.post(
		'/user',
		({ body }) => body,
		{
			body: treaty.schema('User', {
				name: 'string'
			})
		}
	)

export const GET = app.fetch
export const POST = app.fetch
```

:::

2. Create a Treaty client with isomorphic approach

::: code-group

```typescript [lib/eden.ts]
import { treaty } from '@elysia/eden'
import type { app } from '../app/api/[[...slugs]]/route'

// .api to enter /api prefix
export const api =
  // process is defined on server side and build time
  typeof process !== 'undefined'
    ? treaty(app).api
    : treaty<typeof app>('localhost:3000').api
```

It's important that you should use `typeof process` instead of `typeof window` because `window` is not defined during build time, causing hydration error.

:::

3. Use the client in both server and client components

::: code-group

```tsx [app/page.tsx]
import { api } from '../lib/eden'

export default async function Page() {
	const message = await api.get()

	return <h1>Hello, {message}</h1>
}
```

:::

This allows you to have type safety from the frontend to the backend with minimal effort and works with both server and client components, as well as with Incremental Static Regeneration (ISR).

## React Query

We can also use React Query to interact with the Elysia server on the client.

::: code-group

```tsx [src/routes/index.tsx]
import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

import { getTreaty } from './api.$' // [!code ++]

export const Route = createFileRoute('/a')({
	component: App
})

function App() {
	const { data: response } = useQuery({ // [!code ++]
		queryKey: ['get'], // [!code ++]
		queryFn: () => getTreaty().get() // [!code ++]
	}) // [!code ++]

	return response?.data
}
```

::: code-group

This can work with any React Query features like caching, pagination, infinite queries, etc.

***

Please refer to [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers#static-route-handlers) for more information.

---

---
url: 'https://elysiajs.com/integrations/node.md'
---

# Integration with Node.js

Elysia provides a runtime adapter to run Elysia on multiple runtimes, including Node.js.

To run Elysia on Node.js, simply install Node adapter.

::: code-group

```bash [bun]
bun add elysia @elysia/node
```

```bash [pnpm]
pnpm add elysia @elysia/node
```

```bash [npm]
npm install elysia @elysia/node
```

```bash [yarn]
yarn add elysia @elysia/node
```

:::

Then apply the Node adapter to your main Elysia instance.

```typescript
import { Elysia } from 'elysia'
import { node } from '@elysia/node' // [!code ++]

const app = new Elysia({ adapter: node() }) // [!code ++]
	.get('/', () => 'Hello Elysia')
	.listen(3000)
```

This is all you need to run Elysia on Node.js.

### Additional Setup (optional)

For the best experience, we recommend installing `tsx` or `ts-node` with `nodemon`.

`tsx` is a CLI that transpiles TypeScript to JavaScript with hot-reload and several more features you would expect from a modern development environment.

::: code-group

```bash [bun]
bun add -d tsx @types/node typescript
```

```bash [pnpm]
pnpm add -D tsx @types/node typescript
```

```bash [npm]
npm install --save-dev tsx @types/node typescript
```

```bash [yarn]
yarn add -D tsx @types/node typescript
```

:::

Then open your `package.json` file and add the following scripts:

```json
{
   	"scripts": {
  		"dev": "tsx watch src/index.ts",
    	"build": "tsc src/index.ts --outDir dist",
  		"start": "NODE_ENV=production node dist/index.js"
   	}
}
```

These scripts refer to the different stages of developing an application:

* **dev** - Start Elysia in development mode with auto-reload on code changes.
* **build** - Build the application for production use.
* **start** - Start a production Elysia server.

Make sure to create a `tsconfig.json`:

```bash
tsc --init
```

Don't forget to update `tsconfig.json` to set `compilerOptions.strict` to `true`:

```json
{
   	"compilerOptions": {
  		"strict": true
   	}
}
```

This will give the hot reload, JSX support to run Elysia with the similar experience as `bun dev`

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

---

---
url: 'https://elysiajs.com/integrations/nuxt.md'
---

# Integration with Nuxt

We can use [nuxt-elysia](https://github.com/tkesgar/nuxt-elysia), a community plugin for Nuxt, to set up Elysia on Nuxt API routes with Eden Treaty.

1. Install the plugin with the following command:

```bash
bun add elysia @elysia/eden
bun add -d nuxt-elysia
```

2. Add `nuxt-elysia` to your Nuxt config:

```ts
export default defineNuxtConfig({
    modules: [ // [!code ++]
        'nuxt-elysia' // [!code ++]
    ], // [!code ++]
    nitro: { // [!code ++]
        preset: 'Bun' // [!code ++]
    } // [!code ++]
})
```

::: tip
The `nitro.preset: 'Bun'` configuration is required because Elysia runs on Bun runtime. This tells Nuxt's Nitro to use Bun as the server runtime instead of the default Node.js runtime.
:::

3. Create `api.ts` in the project root:

```typescript [api.ts]
export default () => new Elysia() // [!code ++]
  .get('/hello', () => ({ message: 'Hello world!' })) // [!code ++]
```

4. Use Eden Treaty in your Nuxt app:

```vue
<template>
    <div>
        <p>{{ data.message }}</p>
    </div>
</template>
<script setup lang="ts">
const { $api } = useNuxtApp()

const { data } = await useAsyncData(async () => {
    const { data, error } = await $api.hello.get()

    if (error)
        throw new Error('Failed to call API')

    return data
})
</script>
```

This will automatically set up Elysia to run on Nuxt API routes.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Prefix

By default, Elysia will be mounted on **/\_api**, but we can customize it with the `nuxt-elysia` config.

```ts
export default defineNuxtConfig({
	nuxtElysia: {
		path: '/api' // [!code ++]
	}
})
```

This will mount Elysia on **/api** instead of **/\_api**.

For more configuration options, please refer to [nuxt-elysia](https://github.com/tkesgar/nuxt-elysia)

---

---
url: 'https://elysiajs.com/integrations/prisma.md'
---

# Prisma

[Prisma](https://prisma.io) is an ORM that allows us to interact with databases in a type-safe manner.

It provides a way to define your database schema using a Prisma schema file, and then generates TypeScript types based on that schema.

### Prismabox

[Prismabox](https://github.com/m1212e/prismabox) is a library that generate TypeBox or Elysia validation models from Prisma schema.

We can use Prismabox to convert Prisma schema into Elysia validation models, which can then be used to ensure type validation in Elysia.

### How it works:

1. Define your database schema in Prisma Schema.
2. Add `prismabox` generator to generate Elysia schema.
3. Use the converted Elysia validation models to ensure type validation.
4. OpenAPI schema is generated from Elysia validation models.
5. Add [Eden Treaty](/eden/overview) to add type-safety to your frontend.

```
                                                    * ——————————————— *
                                                    |                 |
                                               | -> |  Documentation  |
* ————————— *             * ———————— * OpenAPI |    |                 |
|           |  prismabox  |          | ——————— |    * ——————————————— *
|  Prisma   | —————————-> |  Elysia  |
|           |             |          | ——————— |    * ——————————————— *
* ————————— *             * ———————— *   Eden  |    |                 |
                                               | -> |  Frontend Code  |
												    |                 |
												    * ——————————————— *

```

## Installation

To install Prisma, run the following command:

```bash
bun add @prisma/client prismabox prisma-adapter-bun-sqlite && \
bun add -d prisma
```

## Prisma schema

Assuming you already have a `prisma/schema.prisma`.

We can add a `prismabox` generator to the Prisma schema file as follows:

::: code-group

```ts [prisma/schema.prisma]
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "sqlite"
  // Note: In Prisma 7+, datasource URL is configured in prisma.config.ts (for Prisma CLI),
  // and when using driver adapters you also pass the runtime URL in adapter setup.
}

generator prismabox { // [!code ++]
  provider = "prismabox" // [!code ++]
  typeboxImportDependencyName = "elysia" // [!code ++]
  typeboxImportVariableName = "t" // [!code ++]
  inputModel = true // [!code ++]
  output   = "../generated/prismabox" // [!code ++]
} // [!code ++]

model User {
  id    String  @id @default(cuid())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id    	String  @id @default(cuid())
  title     String
  content   String?
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id])
  authorId  String
}
```

:::

This will generate Elysia validation models in the `generated/prismabox` directory.

Each model will have its own file, and the models will be named based on the Prisma model names.

For example:

* `User` model will be generated to `generated/prismabox/User.ts`
* `Post` model will be generated to `generated/prismabox/Post.ts`

## Using generated models

Then we can import the generated models in our Elysia application:

::: code-group

```ts [src/index.ts]
import { Elysia, t } from 'elysia'

import { PrismaBunSqlite } from 'prisma-adapter-bun-sqlite';
import { PrismaClient } from '../generated/prisma/client' // [!code ++]
import { UserPlain, UserPlainInputCreate } from '../generated/prismabox/User' // [!code ++]

const adapter = new PrismaBunSqlite({ url: process.env.DATABASE_URL });
export const prisma = new PrismaClient({ adapter });

const app = new Elysia()
    .put(
        '/',
        async ({ body }) =>
            prisma.user.create({
                data: body
            }),
        {
            body: UserPlainInputCreate, // [!code ++]
            response: UserPlain // [!code ++]
        }
    )
    .get(
        '/id/:id',
        async ({ params: { id }, status }) => {
            const user = await prisma.user.findUnique({
                where: { id }
            })

            if (!user) return status(404, 'User not found')

            return user
        },
        {
            response: {
                200: UserPlain, // [!code ++]
                404: t.String() // [!code ++]
            }
        }
    )
    .listen(3000)

console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

:::

This allows us to reuse the database schema in Elysia validation models.

***

For more information, please refer to the [Prisma](https://prisma.io), and [Prismabox](https://github.com/m1212e/prismabox) documentation.

---

---
url: 'https://elysiajs.com/integrations/sveltekit.md'
---

# Integration with SvelteKit

With SvelteKit, you can run Elysia on server routes.

1. Create **src/routes/\[...slugs]/+server.ts**.
2. Define an Elysia server.
3. Export a **fallback** function that calls `app.handle`.

```typescript
// src/routes/[...slugs]/+server.ts
import { Elysia, t } from 'elysia';

const app = new Elysia()
    .get('/', 'hello SvelteKit')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

interface WithRequest {
	request: Request
}

export const fallback = ({ request }: WithRequest) => app.handle(request) // [!code ++]
```

You can treat the Elysia server as a normal SvelteKit server route.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Prefix

If you place an Elysia server not in the root directory of the app router, you need to annotate the prefix to the Elysia server.

For example, if you place Elysia server in **src/routes/api/\[...slugs]/+server.ts**, you need to annotate prefix as **/api** to Elysia server.

```typescript
// src/routes/api/[...slugs]/+server.ts
import { Elysia, t } from 'elysia';

const app = new Elysia({ prefix: '/api' }) // [!code ++]
    .get('/', () => 'hi')
    .post('/', ({ body }) => body, {
        body: t.Object({
            name: t.String()
        })
    })

type RequestHandler = (v: { request: Request }) => Response | Promise<Response>

export const fallback: RequestHandler = ({ request }) => app.handle(request)
```

This will ensure that Elysia routing will work properly in any location you place it.

Please refer to [SvelteKit Routing](https://kit.svelte.dev/docs/routing#server) for more information.

---

---
url: 'https://elysiajs.com/integrations/tanstack-start.md'
---

# Integration with TanStack Start

Elysia can run inside TanStack Start server routes.

1. Create **src/routes/api.$.ts**
2. Define an Elysia server
3. Export Elysia handler in **server.handlers**

::: code-group

```typescript [src/routes/api.$.ts]
import { Elysia } from 'elysia'

import { createFileRoute } from '@tanstack/react-router'
import { createIsomorphicFn } from '@tanstack/react-start'

const app = new Elysia({
	prefix: '/api' // [!code ++]
}).get('/', 'Hello Elysia!')

const handle = ({ request }: { request: Request }) => app.fetch(request) // [!code ++]

export const Route = createFileRoute('/api/$')({
	server: {
		handlers: {
			GET: handle, // [!code ++]
			POST: handle // [!code ++]
		}
	}
})
```

:::

Elysia should now be running on **/api**.

We may add additional methods to **server.handlers** to support other HTTP methods as needed.

### pnpm

If you use pnpm, [pnpm doesn't auto install peer dependencies by default](https://github.com/orgs/pnpm/discussions/3995#discussioncomment-1893230) forcing you to install additional dependencies manually.

```bash
pnpm add @sinclair/typebox openapi-types
```

## Eden

We can add [Eden](/eden/overview.html) for **end-to-end type safety** similar to tRPC.

::: code-group

```typescript [src/routes/api.$.ts]
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden' // [!code ++]

import { createFileRoute } from '@tanstack/react-router'
import { createIsomorphicFn } from '@tanstack/react-start'

const app = new Elysia({
	prefix: '/api'
}).get('/', 'Hello Elysia!')

const handle = ({ request }: { request: Request }) => app.fetch(request)

export const Route = createFileRoute('/api/$')({
	server: {
		handlers: {
			GET: handle,
			POST: handle
		}
	}
})

export const getTreaty = createIsomorphicFn() // [!code ++]
	.server(() => treaty(app).api) // [!code ++]
	.client(() => treaty<typeof app>('localhost:3000').api) // [!code ++]
```

:::

Notice that we use **createIsomorphicFn** to create a separate Eden Treaty instance for both the server and client:

1. On the server, Elysia is called directly without HTTP overhead.
2. On the client, we call the Elysia server through HTTP.

In a React component, we can use `getTreaty` to call the Elysia server with type safety.

## Loader Data

Tanstack Start supports **Loader** to fetch data before rendering the component.

::: code-group

```tsx [src/routes/index.tsx]
import { createFileRoute } from '@tanstack/react-router'

import { getTreaty } from './api.$' // [!code ++]

export const Route = createFileRoute('/a')({
	component: App,
	loader: () => getTreaty().get().then((res) => res.data) // [!code ++]
})

function App() {
	const data = Route.useLoaderData() // [!code ++]

	return data
}
```

:::

Calling Elysia in a loader executes it on the server during SSR and doesn’t incur HTTP overhead.
When navigating from one page to another, the loader will run on the client-side, making an HTTP request to the endpoint.

Eden Treaty will ensure type safety on both server and client.

## React Query

We can also use React Query to interact with Elysia server on client.

::: code-group

```tsx [src/routes/index.tsx]
import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

import { getTreaty } from './api.$' // [!code ++]

export const Route = createFileRoute('/a')({
	component: App
})

function App() {
	const { data: response } = useQuery({ // [!code ++]
		queryKey: ['get'], // [!code ++]
		queryFn: () => getTreaty().get() // [!code ++]
	}) // [!code ++]

	return response?.data
}
```

::: code-group

This can work with any React Query features like caching, pagination, infinite queries, etc.

***

Please visit [TanStack Start Documentation](https://tanstack.com/start) for more information about TanStack Start.

---

---
url: 'https://elysiajs.com/tutorial.md'
---

# Welcome to Elysia

It's great to have you here! This playground will help you get started with Elysia interactively.

Unlike traditional backend frameworks, **Elysia can run in a browser**! Although it doesn't support all features, it's a perfect environment for learning and experimentation.

You can check out the API docs by clicking  on the left sidebar.

## What is Elysia

Elysia is an ergonomic framework for humans.

Ok, seriously, Elysia is a backend TypeScript framework that focuses on developer experience and performance.

What makes Elysia different from other frameworks is:

1. Spectacular performance comparable to Golang.
2. Extraordinary TypeScript support with **type soundness**.
3. Built around OpenAPI from the ground up.
4. Offers End-to-end Type Safety like tRPC.
5. Uses Web Standards, allowing you to run your code anywhere like Cloudflare Workers, Deno, Bun, Node.js and more.
6. It is, of course, **designed for humans** first.

Although Elysia has some framework-specific concepts to learn, once users get the hang of it, many find it very enjoyable and intuitive to work with.

## How to use this playground

Playground is divided into 3 sections:

1. Documentation and task on the left side (what you're currently reading).
2. Code editor in the top right
3. Preview, output, and console in the bottom right

## Assignment

For the first assignment, let's modify the code to make the server respond with `"Hello Elysia!"` instead of `"Hello World!"`.

Feel free to look around the code editor and preview section to get familiar with the environment.

\<template #answer>

You can change the response by changing the content inside the `.get` method from `'Hello World!'` to `'Hello Elysia!'`.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', 'Hello World!') // [!code --]
	.get('/', 'Hello Elysia!') // [!code ++]
	.listen(3000)
```

Now Elysia will respond with `"Hello Elysia!"` when you access `/`.

---

---
url: 'https://elysiajs.com/internal/jit-compiler.md'
---

# JIT "Compiler"&#x20;

Elysia is fast and will likely remain *one of the fastest web frameworks for JavaScript* only limited by the speed of the underlying JavaScript engine.

Elysia speed is not only acheived by optimization for specific runtime eg. Bun native features like `Bun.serve.routes`. But also the way Elysia handles route registration and request handling.

Elysia has an **JIT "compiler"** embedded within its core since [Elysia 0.4](/blog/elysia-04) (30 Mar 2023) at (*src/compose.ts*) using `new Function(...)` or also known as `eval(...)`.

The *"compiler"* is not a traditional compiler that translates code from one language to another. Instead, it dynamically generates optimized code for handling requests based on the defined routes and middleware. *(Which is why we put compiler in quotes.)*

When request is made to Elysia application for the first time for each route, Elysia dynamically generates optimized code specifically tailored to handle that route efficiently on the fly avoiding unnecessary overhead as much as possible.

## Static Code Analysis (Sucrose)

*"Sucrose"* is the nick name for the static code analysis module living alongside Elysia's JIT "compiler" at (*src/sucrose.ts*).

To generate this optimized code, the compiler needs a deep understanding of how the route handlers interact with the request and what parts of the request are actually needed.

That's Sucrose's job.

Sucrose read the code without executing it by using `Function.toString()` then perform our own custom pattern-matching to extract useful information about what parts of the request are actually needed by the route handler.

Let's take a look at a simple example:

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
  .patch('/user/:id', ({ params }) => {
	return { id: req.params.id }
  })
```

In this code, we can clearly see that this handler only need a `params` to be parsed.

Sucrose looks at code and tells the *"compiler"* to only parse **params** and skip parsing other parts of the request like **body**, **query**, **headers** entirely as it's not need.

JIT "compiler" then generates code like this:

::: code-group

```ts [Elysia]
function tailoredHandler(request) {
	const context = {
		request,
		params: parseParams(request.url)
	}
	
	return routeHandler(context)
}
```

:::

This approach is entirely different from traditional web frameworks that parse everything by default with a **centralHandler** regardless of whether it's needed or not which looks something like this:

::: code-group

```ts [Traditional Framework]
function centralHandler(request) {
	const context = {
		request,
		body: await parseBody(request),
		query: parseQuery(request.url),
		headers: parseHeader(request.headers),
		// and other stuff
	}

	return routeHandler(context)
}
```

:::

This make Elysia extremely fast as it only does the minimum work required for each route.

### Why not acorn, esprima, or other traditional static analysis tools?

Traditional tools are designed for general-purpose static code analysis and may introduce unnecessary overhead for Elysia's specific use case.

For our purpose, our parser only need to understand a subset of JavaScript syntax specifically *function*. When we think about it, it's only a small part of JavaScript language that is already *parsed and formatted by JavaScript Engine*.

So instead of pulling a general purpose tool, we treat this part as a DSL (that looks like JavaScript) and build specifically for just this part for maximum performance and low-memory usage (compared to AST-based tools).

## Compiler Optimizations

Similar to traditional compilers, Elysia's JIT "compiler" also performs various optimizations to further enhance the performance of the generated code like optimizing control flow based on the specific usage patterns of the route handlers, constant fold, using direct access to properties instead of iterating through objects and arrays when possible, and more.

These optimizations and much smaller optimizations help to reduce the overhead of request handling and improve the overall speed of the application.

### Example: `mapResponse`, `mapCompactResponse`

This is one of the smaller optimizations but can have a significant impact on performance in high-throughput scenarios.

Elysia has two special optimizations for response mapping functions: `mapResponse` and `mapCompactResponse`.

Constructing a `new Response` object can be relatively expensive but for `new Response` without any additional `status` or `headers` is cheaper than constructing a full `Response` object with custom status codes or headers.

When `set` or `status` is not used, Elysia will use `mapCompactResponse` to map a value directly to a `Response` object without the overhead of additional properties.

## Platform Specific Optimization

Elysia is originally made specifically for Bun but also works on [Node.js](/integrations/node), [Deno](/integrations/deno), [Cloudflare Workers](/integrations/cloudflare-workers) and more.

There are a big difference between being **compatible** and being **optimized** for a specific platform.

Elysia can take advantage of platform-specific features and optimizations to further enhance performance, for example `Bun.serve.routes` is used when running on Bun to leverage Bun's native routing capabilities which is written in Zig for maximum performance.

Using the **inline response** for maximum performance for static responses which made Elysia the rank at #14 on [TechEmpower Framework Benchmarks](https://www.techempower.com/benchmarks/#section=data-r23\&hw=ph\&test=plaintext) among the world's fastest backend frameworks.

There are more various smaller optimization like

* using **Bun.websocket** when running on Bun for optimal WebSocket performance
* `Elysia.file` conditionally use `Bun.file` when available for faster file handling
* using `Headers.toJSON()` when running on Bun to reduce overhead when dealing headers

These small optimizations add up to make Elysia extremely fast on its target platforms.

## Overhead of JIT "Compiler"

Elysia JIT *"compiler"* is designed for peak performance in mind. However, the dynamic code generation process does introduce some overhead during the initial request handling for each route.

### Initial Request Overhead

The first time a request is made to a specific route, Elysia needs to analyze the route handler code and generate the optimized code.

This process is relatively **very fast** and usually takes < 0.005ms per route in most cases on a modern CPU and happend only **once per route**. But it is still an overhead.

This process can be moved to the startup phase by settings `precompile: true` to Elysia constructor to eliminate this overhead during the first request in exchange for a slower startup time.

### Memory Usage

The dynamically generated code is stored in memory for subsequent requests. This can lead to increased memory usage, especially for applications with a large number of routes but is relatively low.

### Bigger Bundle Size

The JIT "compiler" and Sucrose module add some additional code to the Elysia core library, which can increase the overall bundle size of the application. However, the performance benefits often outweigh the cost of a slightly larger bundle size.

### Maintainability

The use of dynamic code generation can make the codebase more complex and harder to maintain. Maintainers need to have a good understanding of how the JIT "compiler" works to effectively use and troubleshoot the framework.

### Security Considerations

Using `new Function(...)` or `eval(...)` can introduce security risks **if not handled properly**.

But that's only "if not handled properly" part.

Elysia takes precautions to ensure that the generated code is safe and does not expose vulnerabilities by make sure that only trusted code is executed. The **input is almost never user-controlled** and produced by Elysia (sucrose) itself.

## Libraries that `eval`

Elysia is not the only framework that use `new Function` and `eval`.

[ajv](https://www.npmjs.com/package/ajv) and [TypeBox](https://www.npmjs.com/package/@sinclair/typebox) are an **industry standard** validation library since the early days of Node.js with 895m and 332m downloads/months respectively.

Both of these libraries are using `eval` internally to optimize the performance of their validation code making it [faster its competitors](https://moltar.github.io/typescript-runtime-type-benchmarks/).

Elysia basically expands this beyond input validation into a whole backend framework for maximum performance. In fact, Elysia also use TypeBox for input validation, so every corner of the libraries is entirely runs on `eval`.

## Opts out

Elysia JIT compilation is enabled by default but can be opt out entirely by running in a dynamic mode:

```ts
new Elysia({ aot: false })
```

Although, it's not recommended because there are some features missing without JIT compilation, eg. `trace`.

## Afterword

With all of these *overkills* optimization, Elysia manages to have *almost* zero overhead and the only limiting factor is the speed of the underlying JavaScript engine itself.

Despite the maintainability challenges, the trade-offs made by Elysia's JIT "compiler" are worth it for the significant performance gains it provides and aligns with our goal to provide a fast foundation for building high-performance server.

This can also be seen as a differentiating factor for Elysia compared to other web frameworks that may not prioritize performance to the same extent because it's extremely hard to do properly.

We also has a [short 6-pages research paper we published to ACM Digital Library](https://dl.acm.org/doi/10.1145/3605098.3636068) about Elysia's JIT "compiler" and its performance optimizations.

For over years of Elysia existence, **we almost never saw a valid benchmark where Elysia is not the fastest framework** available on a platform except using a FFI/native binding (eg. Rust, Go, Zig) with a valid benchmark.

Which is still relatively a very hard to beat because of serialization/deserialization overhead. There are some cases like uWebSocket which is written in C++ with JavaScript binding, making it extremely fast that outperform Elysia.

But despite all odds, we think it's **worth it**.

---

---
url: 'https://elysiajs.com/plugins/jwt.md'
---

# JWT Plugin

This plugin adds support for using JWT in Elysia handlers.

Install with:

```bash
bun add @elysia/jwt
```

Then use it:

::: code-group

```typescript [cookie]
import { Elysia } from 'elysia'
import { jwt } from '@elysia/jwt'

const app = new Elysia()
    .use(
        jwt({
            name: 'jwt',
            secret: 'Fischl von Luftschloss Narfidort'
        })
    )
    .get('/sign/:name', async ({ jwt, params: { name }, cookie: { auth } }) => {
    	const value = await jwt.sign({ name })

        auth.set({
            value,
            httpOnly: true,
            maxAge: 7 * 86400,
            path: '/profile',
        })

        return `Sign in as ${value}`
    })
    .get('/profile', async ({ jwt, status, cookie: { auth } }) => {
        const profile = await jwt.verify(auth.value)

        if (!profile)
            return status(401, 'Unauthorized')

        return `Hello ${profile.name}`
    })
    .listen(3000)
```

```typescript [headers]
import { Elysia } from 'elysia'
import { jwt } from '@elysia/jwt'

const app = new Elysia()
    .use(
        jwt({
            name: 'jwt',
            secret: 'Fischl von Luftschloss Narfidort'
        })
    )
    .get('/sign/:name', ({ jwt, params: { name } }) => {
    	return jwt.sign({ name })
    })
    .get('/profile', async ({ jwt, error, headers: { authorization } }) => {
        const profile = await jwt.verify(authorization)

        if (!profile)
            return status(401, 'Unauthorized')

        return `Hello ${profile.name}`
    })
    .listen(3000)
```

:::

## Config

This plugin extends config from [jose](https://github.com/panva/jose).

Below is a config that is accepted by the plugin.

### name

Name to register `jwt` function as.

For example, `jwt` function will be registered with a custom name.

```typescript
app
    .use(
        jwt({
            name: 'myJWTNamespace',
            secret: process.env.JWT_SECRETS!
        })
    )
    .get('/sign/:name', ({ myJWTNamespace, params }) => {
        return myJWTNamespace.sign(params)
    })
```

Because some might need to use multiple `jwt` with different configs in a single server, explicitly registering the JWT function with a different name is needed.

### secret

The private key to sign JWT payload with.

### schema

Strict type validation for JWT payload.

***

Below is a config that extends from [cookie](https://npmjs.com/package/cookie)

### alg

@default `HS256`

Signing Algorithm to sign JWT payload with.

Possible properties for jose are:
HS256
HS384
HS512
PS256
PS384
PS512
RS256
RS384
RS512
ES256
ES256K
ES384
ES512
EdDSA

### iss

The issuer claim identifies the principal that issued the JWT as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.1)

TLDR; is usually (the domain) name of the signer.

### sub

The subject claim identifies the principal that is the subject of the JWT.

The claims in a JWT are normally statements about the subject as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.2)

### aud

The audience claim identifies the recipients that the JWT is intended for.

Each principal intended to process the JWT MUST identify itself with a value in the audience claim as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.3)

### jti

JWT ID claim provides a unique identifier for the JWT as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.7)

### nbf

The "not before" claim identifies the time before which the JWT must not be accepted for processing as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.5)

### exp

The expiration time claim identifies the expiration time on or after which the JWT MUST NOT be accepted for processing as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.4)

### iat

The "issued at" claim identifies the time at which the JWT was issued.

This claim can be used to determine the age of the JWT as per [RFC7519](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.6)

### b64

This JWS Extension Header Parameter modifies the JWS Payload representation and the JWS Signing input computation as per [RFC7797](https://www.rfc-editor.org/rfc/rfc7797).

### kid

A hint indicating which key was used to secure the JWS.

This parameter allows originators to explicitly signal a change of key to recipients as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.4)

### x5t

(X.509 certificate SHA-1 thumbprint) header parameter is a base64url-encoded SHA-1 digest of the DER encoding of the X.509 certificate [RFC5280](https://www.rfc-editor.org/rfc/rfc5280) corresponding to the key used to digitally sign the JWS as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.7)

### x5c

(X.509 certificate chain) header parameter contains the X.509 public key certificate or certificate chain [RFC5280](https://www.rfc-editor.org/rfc/rfc5280) corresponding to the key used to digitally sign the JWS as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.6)

### x5u

(X.509 URL) header parameter is a URI [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) that refers to a resource for the X.509 public key certificate or certificate chain \[RFC5280] corresponding to the key used to digitally sign the JWS as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.5)

### jwk

The "jku" (JWK Set URL) Header Parameter is a URI \[RFC3986] that refers to a resource for a set of JSON-encoded public keys, one of which corresponds to the key used to digitally sign the JWS.

The keys MUST be encoded as a JWK Set \[JWK] as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.2)

### typ

The `typ` (type) Header Parameter is used by JWS applications to declare the media type \[IANA.MediaTypes] of this complete JWS.

This is intended for use by the application when more than one kind of object could be present in an application data structure that can contain a JWS as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.9)

### ctr

Content-Type parameter is used by JWS applications to declare the media type \[IANA.MediaTypes] of the secured content (the payload).

This is intended for use by the application when more than one kind of object could be present in the JWS Payload as per [RFC7515](https://www.rfc-editor.org/rfc/rfc7515#section-4.1.9)

## Handler

Below are the values added to the handler.

### jwt.sign

A dynamic object of collection related to use with JWT registered by the JWT plugin.

Type:

```typescript
sign: (payload: JWTPayloadSpec): Promise<string>
```

`JWTPayloadSpec` accepts the same value as [JWT config](#config)

### jwt.verify

Verify payload with the provided JWT config

Type:

```typescript
verify(payload: string) => Promise<JWTPayloadSpec | false>
```

`JWTPayloadSpec` accepts the same value as [JWT config](#config)

## Pattern

Below you can find the common patterns to use the plugin.

## Set JWT expiration date

By default, the config is passed to `setCookie` and inherits its value.

```typescript
const app = new Elysia()
    .use(
        jwt({
            name: 'jwt',
            secret: 'kunikuzushi',
            exp: '7d'
        })
    )
    .get('/sign/:name', async ({ jwt, params }) => jwt.sign(params))
```

This will sign JWT with an expiration date of the next 7 days.

---

---
url: 'https://elysiajs.com/key-concept.md'
---

# Key Concept&#x20;

Elysia has every important concept that you need to understand.

This page covers most concepts that you should know before getting started.

## Encapsulation&#x20;

Elysia lifecycle methods are **encapsulated** to its own instance only.

Which means if you create a new instance, it will not share the lifecycle methods with others.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(({ cookie }) => {
		throwIfNotSignIn(cookie)
	})
	.get('/profile', () => 'Hi there!')

const app = new Elysia()
	.use(profile)
	// ⚠️ This will NOT have sign in check
	.patch('/rename', ({ body }) => updateProfile(body))
```

In this example, the `isSignIn` check will only apply to `profile` but not `app`.

> Try changing the path in the URL bar to **/rename** and see the result

**Elysia isolates lifecycle by default** unless explicitly stated. This is similar to **export** in JavaScript, where you need to export the function to make it available outside the module.

To **"export"** the lifecycle to other instances, you must add specify the scope.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(
		{ as: 'global' }, // [!code ++]
		({ cookie }) => {
			throwIfNotSignIn(cookie)
		}
	)
	.get('/profile', () => 'Hi there!')

const app = new Elysia()
	.use(profile)
	// This has sign in check
	.patch('/rename', ({ body }) => updateProfile(body))
```

Casting lifecycle to **"global"** will export lifecycle to **every instance**.

Learn more about this in [scope](/essential/plugin.html#scope-level).

## Method Chaining&#x20;

Elysia code should **ALWAYS** use method chaining.

This is **important to ensure type safety**.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .state('build', 1)
    // Store is strictly typed // [!code ++]
    .get('/', ({ store: { build } }) => build)
                        // ^?
    .listen(3000)
```

In the code above, **state** returns a new **ElysiaInstance** type, adding a typed `build` property.

### Without method chaining

As Elysia type system is complex, every method in Elysia returns a new type reference.

Without using method chaining, Elysia doesn't save these new types, leading to no type inference.

```typescript twoslash
// @errors: 2339
import { Elysia } from 'elysia'

const app = new Elysia()

app.state('build', 1)

app.get('/', ({ store: { build } }) => build)

app.listen(3000)
```

We recommend to **always use method chaining** to provide an accurate type inference.

## Dependency&#x20;

Elysia, by design, is composed of multiple mini Elysia apps which can run **independently** like microservices that communicate with each other.

Each Elysia instance is independent and **can run as a standalone server**.

When an instance needs to use another instance's service, you **must explicitly declare the dependency**.

```ts twoslash
// @errors: 2339
import { t } from 'elysia'

abstract class Auth {
	static getProfile() {
		return {
			name: 'Elysia User'
		}
	}

	static models = {
		user: t.Object({
			name: t.String()
		})
	} as const
}
// ---cut---
import { Elysia } from 'elysia'

const auth = new Elysia()
	.decorate('Auth', Auth)
	.model(Auth.models)

const main = new Elysia()
 	// ❌ 'auth' is missing
	.get('/', ({ Auth }) => Auth.getProfile())
	// auth is required to use Auth's service
	.use(auth) // [!code ++]
	.get('/profile', ({ Auth }) => Auth.getProfile())
//                                        ^?



// ---cut-after---
```

This is similar to **Dependency Injection** where each instance must declare its dependencies.

This approach forces you to be explicit about dependencies, allowing better tracking and modularity.

### Deduplication&#x20;

By default, each plugin will be re-executed **every time** applying to another instance.

To prevent this, Elysia can deduplicate lifecycle with **a unique identifier** using `name` and optional `seed` property.

```ts
import { Elysia } from 'elysia'

// `name` is a unique identifier
const ip = new Elysia({ name: 'ip' }) // [!code ++]
	.derive(
		{ as: 'global' },
		({ server, request }) => ({
			ip: server?.requestIP(request)
		})
	)
	.get('/ip', ({ ip }) => ip)

const router1 = new Elysia()
	.use(ip)
	.get('/ip-1', ({ ip }) => ip)

const router2 = new Elysia()
	.use(ip)
	.get('/ip-2', ({ ip }) => ip)

const server = new Elysia()
	.use(router1)
	.use(router2)
```

Adding the `name` and optional `seed` to the instance will make it a unique identifier, preventing it from being called multiple times.

Learn more about this in [plugin deduplication](/essential/plugin.html#plugin-deduplication).

### Global vs Explicit Dependency

There are some cases where global dependency makes more sense than an explicit one.

**Global** plugin example:

* **Plugins that don't add types** - eg. cors, compress, helmet
* Plugins that add global lifecycle that no instance should have control over - eg. tracing, logging

Example use cases:

* OpenAPI/Open - Global document
* OpenTelemetry - Global tracer
* Logging - Global logger

In cases like this, it makes more sense to create it as global dependency instead of applying it to every instance.

However, if your dependency doesn't fit into these categories, it's recommended to use **explicit dependency** instead.

**Explicit dependency** example:

* **Plugins that add types** - eg. macro, state, model
* Plugins that add business logic that an instance can interact with - eg. Auth, Database

Example use cases:

* State management - eg. Store, Session
* Data modeling - eg. ORM, ODM
* Business logic - eg. Auth, Database
* Feature module - eg. Chat, Notification

## Order of code&#x20;

The order of Elysia's life-cycle code is very important.

Because events will only apply to routes **after** they are registered.

If you put the onError before plugin, plugin will not inherit the onError event.

```typescript
import { Elysia } from 'elysia'

new Elysia()
 	.onBeforeHandle(() => {
        console.log('1')
    })
	.get('/', () => 'hi')
    .onBeforeHandle(() => {
        console.log('2')
    })
    .listen(3000)
```

Console should log the following:

```bash
1
```

Notice that it doesn't log **2**, because the event is registered after the route so it is not applied to the route.

Learn more about this in [order of code](/essential/life-cycle.html#order-of-code).

## Type Inference

Elysia has a complex type system that allows you to infer types from the instance.

```ts twoslash
import { Elysia, t } from 'elysia'

const app = new Elysia()
	.post('/', ({ body }) => body, {
                // ^?




		body: t.Object({
			name: t.String()
		})
	})
```

You should **always use an inline function** to provide an accurate type inference.

If you need to apply a separate function, eg. MVC's controller pattern, it's recommended to destructure properties from inline function to prevent unnecessary type inference as follows:

```ts
import { Elysia, t } from 'elysia'

abstract class Controller {
	static greet({ name }: { name: string }) {
		return 'hello ' + name
	}
}

const app = new Elysia()
	.post('/', ({ body }) => Controller.greet(body), {
		body: t.Object({
			name: t.String()
		})
	})
```

See [Best practice: MVC Controller](/essential/best-practice.html#controller).

### TypeScript

We can get type definitions for every Elysia/TypeBox type by accessing the `static` property as follows:

```ts twoslash
import { t } from 'elysia'

const MyType = t.Object({
	hello: t.Literal('Elysia')
})

type MyType = typeof MyType.static
//    ^?
```

This allows Elysia to infer and provide types automatically, reducing the need to declare duplicate schemas.

A single Elysia/TypeBox schema can be used for:

* Runtime validation
* Data coercion
* TypeScript type
* OpenAPI schema

This allows us to make a schema as a **single source of truth**.

---

---
url: 'https://elysiajs.com/tutorial/getting-started/life-cycle.md'
---

# Lifecycle

Lifecycle **hooks** are functions that are executed on a specific event during the request-response cycle.

They allow you to run custom logic at a certain point

* request - when a request is received
* beforeHandle - before executing a handler
* afterResponse - after a response is sent, etc.
* error - when an error occurs

This can be useful for tasks like logging, authentication, etc.

To register a lifecycle hook, you can pass it as the 3rd argument of a route method:

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/1', () => 'Hello Elysia!')
	.get('/auth', () => {
		console.log('This is executed after "beforeHandle"')

		return 'Oh you are lucky!'
	}, {
		beforeHandle({ request, status }) {
			console.log('This is executed before handler')

			if(Math.random() <= 0.5)
				return status(418)
		}
	})
	.get('/2', () => 'Hello Elysia!')
```

Here we use `status(418)` which is the "I'm a teapot" status code. You can also use the string name directly: `status("I'm a teapot")`. See Status for more on using status codes.

When `beforeHandle` returns a value, it will skip the handler and return the value instead.

This is useful for things like authentication, where you want to return a `401 Unauthorized` response if the user is not authenticated.

See Life Cycle, Before Handle for a more detailed explanation.

## Hook

A function that intercepts the **lifecycle event**. because a function **"hooks"** into the lifecycle event

Hook can be categorized into 2 types:

1. Local Hook - execute on a specific route
2. Interceptor Hook - execute on every route **after the hook is registered**

## Local Hook

A local hook is executed on a specific route.

To use a local hook, you can inline hook into a route handler:

```typescript
// Similar to previous code snippet
import { Elysia } from 'elysia'

new Elysia()
	.get('/1', () => 'Hello Elysia!')
	.get('/auth', () => {
		console.log('Run after "beforeHandle"')

		return 'Oh you are lucky!'
	}, {
		// This is a Local Hook
		beforeHandle({ request, status }) {
			console.log('Run before handler')

			if(Math.random() <= 0.5)
				return status(418)
		}
	})
	.get('/2', () => 'Hello Elysia!')
```

## Interceptor Hook

Register hook into every **handler that came after the hook is called** for the current instance only.

To add an interceptor hook, you can use `.on` followed by a lifecycle event:

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/1', () => 'Hello Elysia!')
	.onBeforeHandle(({ request, status }) => {
		console.log('This is executed before handler')

		if(Math.random() <= 0.5)
			return status(418)
	})
	// "beforeHandle" is applied
	.get('/auth', () => {
		console.log('This is executed after "beforeHandle"')

		return 'Oh you are lucky!'
	})
	// "beforeHandle" is also applied
	.get('/2', () => 'Hello Elysia!')
```

Unlike Local Hook, Interceptor Hook will add the hook to every route that came after the hook is registered.

## Assignment

Let's put 2 types of hooks into practice.

\<template #answer>

We can use `beforeHandle` to intercept the request before it reaches the handler, and return a response with `status` method.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onBeforeHandle(({ query: { name }, status }) => {
		if(!name) return status(401)
	})
	.get('/auth', ({ query: { name = 'anon' } }) => {
		return `Hello ${name}!`
	})
	.get('/profile', ({ query: { name = 'anon' } }) => {
		return `Hello ${name}!`
	})
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/essential/life-cycle.md'
---

# Lifecycle&#x20;

Instead of a sequential process, Elysia's request handling is divided into multiple stages called **lifecycle events**.

It's designed to separate the process into distinct phases based on their responsibility without interfering with each others.

Here are the lifecycle events in order:

***

Elysia's lifecycle can be illustrated as the following.
![Elysia Life Cycle Graph](/assets/lifecycle-chart.svg)

> Click on image to enlarge

## Why

Let’s say we want to send back some HTML.

Normally, we’d set the **"Content-Type"** header to **"text/html"** so the browser can render it.

But manually setting one for each route is tedious.

Instead, what if the framework could detect when a response is HTML and automatically set the header for you? That’s where the idea of a lifecycle comes in.

## Hook

Each function that intercepts the **lifecycle event** is called a **"hook"**.

(as the function **"hooks"** into the lifecycle event)

Hooks can be categorized into 2 types:

1. [Local Hook](#local-hook): Execute on a specific route
2. [Interceptor Hook](#interceptor-hook): Execute on every route **after the hook is registered**

::: tip
The hook will accept the same Context as a handler; you can imagine adding a route handler but at a specific point.
:::

## Local Hook

A local hook is executed on a specific route.

To use a local hook, you can inline hook into a route handler:

```typescript
import { Elysia } from 'elysia'
import { isHtml } from '@elysia/html'

new Elysia()
    .get('/', () => '<h1>Hello World</h1>', {
        afterHandle({ responseValue, set }) {
            if (isHtml(responseValue))
                set.headers['Content-Type'] = 'text/html; charset=utf8'
        }
    })
    .get('/hi', () => '<h1>Hello World</h1>')
    .listen(3000)
```

The response should be listed as follows:

| Path | Content-Type             |
| ---- | ------------------------ |
| /    | text/html; charset=utf8  |
| /hi  | text/plain; charset=utf8 |

## Interceptor Hook

Register hook into every handler **of the current instance** that came after.

To add an interceptor hook, you can use `.on` followed by a lifecycle event in camelCase:

```typescript
import { Elysia } from 'elysia'
import { isHtml } from '@elysia/html'

new Elysia()
    .get('/none', () => '<h1>Hello World</h1>')
    .onAfterHandle(({ responseValue, set }) => {
        if (isHtml(responseValue))
            set.headers['Content-Type'] = 'text/html; charset=utf8'
    })
    .get('/', () => '<h1>Hello World</h1>')
    .get('/hi', () => '<h1>Hello World</h1>')
    .listen(3000)
```

The response should be listed as follows:

| Path  | Content-Type             |
| ----- | ------------------------ |
| /none | text/**plain**; charset=utf8 |
| /     | text/**html**; charset=utf8  |
| /hi   | text/**html**; charset=utf8  |

Events from other plugins are also applied to the route, so the order of code is important.

## Order of code

Event will only apply to routes **after** it is registered.

If you put the `onError` before plugin, plugin will not inherit the `onError` event.

```typescript
import { Elysia } from 'elysia'

new Elysia()
 	.onBeforeHandle(() => {
        console.log('1')
    })
	.get('/', () => 'hi')
    .onBeforeHandle(() => {
        console.log('2')
    })
    .listen(3000)
```

Console should log the following:

```bash
1
```

Notice that it doesn't log **2**, because the event is registered after the route so it is not applied to the route.

This also applies to the plugin.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onBeforeHandle(() => {
		console.log('1')
	})
	.use(someRouter)
	.onBeforeHandle(() => {
		console.log('2')
	})
	.listen(3000)
```

In this example, only **1** will be logged because the event is registered after the plugin.

Every event follows the same rule except `onRequest`.
Because onRequest happens on request, it doesn't know which route to apply it to, so it's a global event

## Request

The first lifecycle event to be executed for every new request.

As `onRequest` is designed to provide only the most crucial context to reduce overhead, it is recommended to use in the following scenarios:

* Caching
* Rate Limiter / IP/Region Lock
* Analytic
* Provide custom header, eg. CORS

#### Example

Below is a pseudocode to enforce rate-limits on a certain IP address.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .use(rateLimiter)
    .onRequest(({ rateLimiter, ip, set, status }) => {
        if (rateLimiter.check(ip)) return status(420, 'Enhance your calm')
    })
    .get('/', () => 'hi')
    .listen(3000)
```

If a value is returned from `onRequest`, it will be used as the response and the rest of the lifecycle will be skipped.

### Pre Context

The `onRequest` context is typed as `PreContext`, a minimal representation of `Context` with the following attributes:
request: `Request`

* set: `Set`
* store
* decorators

Context doesn't provide `derived` value because derive is based on `onTransform` event.

## Parse

Parse is an equivalent of **body parser** in Express.

A function to parse the body; the return value will be appended to `Context.body`. If not, Elysia will continue iterating through additional parser functions assigned by `onParse` until either body is assigned or all parsers have been executed.

By default, Elysia will parse the body with content-type of:

* `text/plain`
* `application/json`
* `multipart/form-data`
* `application/x-www-form-urlencoded`

It's recommended to use the `onParse` event to provide a custom body parser that Elysia doesn't provide.

#### Example

Below is an example code to retrieve value based on custom headers.

```typescript
import { Elysia } from 'elysia'

new Elysia().onParse(({ request, contentType }) => {
    if (contentType === 'application/custom-type') return request.text()
})
```

The returned value will be assigned to `Context.body`. If not, Elysia will continue iterating through additional parser functions from **onParse** stack until either body is assigned or all parsers have been executed.

### Context

`onParse` context extends from `Context` with the following additional properties:

* contentType: Content-Type header of the request

All of the context is based on normal context and can be used like normal context in route handler.

### Parser

By default, Elysia will try to determine body parsing function ahead of time and pick the most suitable function to speed up the process.

Elysia is able to determine that body function by reading `body`.

Take a look at this example:

```typescript
import { Elysia, t } from 'elysia'

new Elysia().post('/', ({ body }) => body, {
    body: t.Object({
        username: t.String(),
        password: t.String()
    })
})
```

Elysia reads the body schema and finds that the type is entirely an object, so it's likely that the body will be JSON. Elysia then picks the JSON body parser function ahead of time and tries to parse the body.

Here are the criteria that Elysia uses to select the body parser type:

* `application/json`: body typed as `t.Object`
* `multipart/form-data`: body typed as `t.Object`, and is 1 level deep with `t.File`
* `application/x-www-form-urlencoded`: body typed as `t.URLEncoded`
* `text/plain`: other primitive type

This allows Elysia to optimize body parser ahead of time, and reduce overhead in compile time.

### Explicit Parser

However, in some scenarios if Elysia fails to pick the correct body parser function, we can explicitly tell Elysia to use a certain function by specifying `type`.

```typescript
import { Elysia } from 'elysia'

new Elysia().post('/', ({ body }) => body, {
    // Short form of application/json
    parse: 'json'
})
```

This allows us to control Elysia behavior for picking body parser function to fit our needs in a complex scenario.

`type` may be one of the following:

```typescript
type ContentType = |
    // Shorthand for 'text/plain'
    | 'text'
    // Shorthand for 'application/json'
    | 'json'
    // Shorthand for 'multipart/form-data'
    | 'formdata'
    // Shorthand for 'application/x-www-form-urlencoded'
    | 'urlencoded'
    // Skip body parsing entirely
    | 'none'
    | 'text/plain'
    | 'application/json'
    | 'multipart/form-data'
    | 'application/x-www-form-urlencoded'
```

### Skip Body Parsing

When you need to integrate a third-party library with an HTTP handler like `trpc` or `orpc`, and it throws `Body is already used`.

This is because Web Standard Request can be parsed only once.

Both Elysia and the third-party library both has its own body parser, so you can skip body parsing on Elysia side by specifying `parse: 'none'`

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.post(
		'/',
		({ request }) => library.handle(request),
		{
			parse: 'none'
		}
	)
```

### Custom Parser

You can register a custom parser with `parser`:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .parser('custom', ({ request, contentType }) => {
        if (contentType === 'application/elysia') return request.text()
    })
    .post('/', ({ body }) => body, {
        parse: ['custom', 'json']
    })
```

## Transform

Executed just before **Validation** process, designed to mutate context to conform with the validation or appending new value.

It's recommended to use transform for the following:

* Mutating the existing context to conform with validation.
* `derive` is based on `onTransform` with support for providing type.

#### Example

Below is an example of using transform to mutate params to be numeric values.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        }),
        transform({ params }) {
            const id = +params.id

            if (!Number.isNaN(id)) params.id = id
        }
    })
    .listen(3000)
```

## Derive

Append new value to context directly **before validation**. It's stored in the same stack as **transform**.

Unlike **state** and **decorate**, which assign values before the server starts, **derive** assigns a property when each request happens. This allows us to extract a piece of information into a property.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .derive(({ headers }) => {
        const auth = headers['Authorization']

        return {
            bearer: auth?.startsWith('Bearer ') ? auth.slice(7) : null
        }
    })
    .get('/', ({ bearer }) => bearer)
```

Because **derive** is assigned once a new request starts, **derive** can access Request properties like **headers**, **query**, **body** where **store**, and **decorate** can't.

Unlike **state** and **decorate**, properties assigned by **derive** are unique and not shared with other requests.

::: tip
You might want to use [resolve](#resolve) instead of derive in most cases.

Resolve is similar to derive but execute after validation. This makes resolve more secure as we can validate the incoming data before using it to derive new properties.
:::

### Queue

`derive` and `transform` are stored in the same queue.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onTransform(() => {
        console.log(1)
    })
    .derive(() => {
        console.log(2)

        return {}
    })
```

The console should log as the following:

```bash
1
2
```

## Before Handle

Executed after validation and before the main route handler.

Designed to provide a custom validation to provide a specific requirement before running the main handler.

If a value is returned, the route handler will be skipped.

It's recommended to use Before Handle in the following situations:

* Restricted access check: authorization, user sign-in
* Custom request requirement over data structure

#### Example

Below is an example of using the before handle to check for user sign-in.

```typescript
import { Elysia } from 'elysia'
import { validateSession } from './user'

new Elysia()
    .get('/', () => 'hi', {
        beforeHandle({ set, cookie: { session }, status }) {
            if (!validateSession(session.value)) return status(401)
        }
    })
    .listen(3000)
```

The response should be listed as follows:

| Is signed in | Response     |
| ------------ | ------------ |
| ❌           | Unauthorized |
| ✅           | Hi           |

### Guard

When we need to apply the same before handle to multiple routes, we can use `guard` to apply the same before handle to multiple routes.

```typescript
import { Elysia } from 'elysia'
import { signUp, signIn, validateSession, isUserExists } from './user'

new Elysia()
    .guard(
        {
            beforeHandle({ set, cookie: { session }, status }) {
                if (!validateSession(session.value)) return status(401)
            }
        },
        (app) =>
            app
                .get('/user/:id', ({ body }) => signUp(body))
                .post('/profile', ({ body }) => signIn(body), {
                    beforeHandle: isUserExists
                })
    )
    .get('/', () => 'hi')
    .listen(3000)
```

## Resolve

Append new value to context **after validation**. It's stored in the same stack as **beforeHandle**.

Resolve syntax is identical to [derive](#derive), below is an example of retrieving a bearer header from the Authorization plugin.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .guard(
        {
            headers: t.Object({
                authorization: t.TemplateLiteral('Bearer ${string}')
            })
        },
        (app) =>
            app
                .resolve(({ headers: { authorization } }) => {
                    return {
                        bearer: authorization.split(' ')[1]
                    }
                })
                .get('/', ({ bearer }) => bearer)
    )
    .listen(3000)
```

Using `resolve` and `onBeforeHandle` is stored in the same queue.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onBeforeHandle(() => {
        console.log(1)
    })
    .resolve(() => {
        console.log(2)

        return {}
    })
    .onBeforeHandle(() => {
        console.log(3)
    })
```

The console should log as the following:

```bash
1
2
3
```

Same as **derive**, properties assigned by **resolve** are unique and not shared with other requests.

### Guard resolve

As resolve is not available in local hook, it's recommended to use guard to encapsulate the **resolve** event.

```typescript
import { Elysia } from 'elysia'
import { isSignIn, findUserById } from './user'

new Elysia()
    .guard(
        {
            beforeHandle: isSignIn
        },
        (app) =>
            app
                .resolve(({ cookie: { session } }) => ({
                    userId: findUserById(session.value)
                }))
                .get('/profile', ({ userId }) => userId)
    )
    .listen(3000)
```

## After Handle

Execute after the main handler, for mapping a returned value of **before handle** and **route handler** into a proper response.

It's recommended to use After Handle in the following situations:

* Transform requests into a new value, eg. Compression, Event Stream
* Add custom headers based on the response value, eg. **Content-Type**

#### Example

Below is an example of using the after handle to add HTML content type to response headers.

```typescript
import { Elysia } from 'elysia'
import { isHtml } from '@elysia/html'

new Elysia()
    .get('/', () => '<h1>Hello World</h1>', {
        afterHandle({ response, set }) {
            if (isHtml(response))
                set.headers['content-type'] = 'text/html; charset=utf8'
        }
    })
    .get('/hi', () => '<h1>Hello World</h1>')
    .listen(3000)
```

The response should be listed as follows:

| Path | Content-Type             |
| ---- | ------------------------ |
| /    | text/html; charset=utf8  |
| /hi  | text/plain; charset=utf8 |

### Returned Value

If a value is returned After Handle will use a return value as a new response value unless the value is **undefined**

The above example could be rewritten as the following:

```typescript
import { Elysia } from 'elysia'
import { isHtml } from '@elysia/html'

new Elysia()
    .get('/', () => '<h1>Hello World</h1>', {
        afterHandle({ response, set }) {
            if (isHtml(response)) {
                set.headers['content-type'] = 'text/html; charset=utf8'
                return new Response(response)
            }
        }
    })
    .get('/hi', () => '<h1>Hello World</h1>')
    .listen(3000)
```

Unlike **beforeHandle**, after a value is returned from **afterHandle**, the iteration of **afterHandle will NOT be skipped**.

### Context

`onAfterHandle` context extends from `Context` with the additional property of `response`, which is the response to return to the client.

The `onAfterHandle` context is based on the normal context and can be used like the normal context in route handlers.

## Map Response

Executed just after **"afterHandle"**, designed to provide custom response mapping.

It's recommended to use transform for the following:

* Compression
* Map value into a Web Standard Response

#### Example

Below is an example of using mapResponse to provide Response compression.

```typescript
import { Elysia } from 'elysia'

const encoder = new TextEncoder()

new Elysia()
    .mapResponse(({ responseValue, set }) => {
        const isJson = typeof responseValue === 'object'

        const text = isJson
            ? JSON.stringify(responseValue)
            : (responseValue?.toString() ?? '')

        set.headers['Content-Encoding'] = 'gzip'

        return new Response(Bun.gzipSync(encoder.encode(text)), {
            headers: {
                'Content-Type': `${
                    isJson ? 'application/json' : 'text/plain'
                }; charset=utf-8`
            }
        })
    })
    .get('/text', () => 'mapResponse')
    .get('/json', () => ({ map: 'response' }))
    .listen(3000)
```

Like **parse** and **beforeHandle**, after a value is returned, the next iteration of **mapResponse** will be skipped.

Elysia automatically handles merging **set.headers** from **mapResponse**. You don't need to worry about appending **set.headers** to the Response manually.

## On Error (Error Handling)

Designed for error handling. It will be executed when an error is thrown in any lifecycle.

It's recommended to use **onError** in the following situations:

* providing custom error messages
* fail-safe handling, an error handler, or retrying a request
* logging and analytics

#### Example

Elysia catches all the errors thrown in the handler, classifies the error code, and pipes them to `onError` middleware.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onError(({ error }) => {
        return new Response(error.toString())
    })
    .get('/', () => {
        throw new Error('Server is during maintenance')

        return 'unreachable'
    })
```

With `onError` we can catch and transform the error into a custom error message.

::: tip
It's important that `onError` must be registered before the handler you want to apply it to.
:::

### Custom 404 message

For example, returning custom 404 messages:

```typescript
import { Elysia, NotFoundError } from 'elysia'

new Elysia()
    .onError(({ code, status, set }) => {
        if (code === 'NOT_FOUND') return status(404, 'Not Found :(')
    })
    .post('/', () => {
        throw new NotFoundError()
    })
    .listen(3000)
```

### Context

`onError` context extends from `Context` with the following additional properties:

* **error**: A value that was thrown
* **code**: *Error Code*

### Error Code

Elysia error code consists of:

* **NOT\_FOUND**
* **PARSE**
* **VALIDATION**
* **INTERNAL\_SERVER\_ERROR**
* **INVALID\_COOKIE\_SIGNATURE**
* **INVALID\_FILE\_TYPE**
* **UNKNOWN**
* **number** (based on HTTP Status)

By default, the thrown error code is `UNKNOWN`.

::: tip
If no error response is returned, the error will be returned using `error.name`.
:::

### Local Error

Same as other lifecycle events, we provide an error into a [scope](/essential/plugin.html#scope) using guard:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', () => 'Hello', {
        beforeHandle({ set, request: { headers }, error }) {
            if (!isSignIn(headers)) throw error(401)
        },
        error() {
            return 'Handled'
        }
    })
    .listen(3000)
```

## After Response

Executed after the response sent to the client.

It's recommended to use **After Response** in the following situations:

* Clean up response
* Logging and analytics

#### Example

Below is an example of using the response handle to check for user sign-in.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .onAfterResponse(() => {
        console.log('Response', performance.now())
    })
    .listen(3000)
```

Console should log as the following:

```bash
Response 0.0000
Response 0.0001
Response 0.0002
```

### Response

Similar to [Map Response](#map-resonse), `afterResponse` also accepts a `responseValue` value.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onAfterResponse(({ responseValue }) => {
		console.log(responseValue)
	})
	.get('/', () => 'Hello')
	.listen(3000)
```

`response` from `onAfterResponse` is not a Web Standard `Response` but is a value that is returned from the handler.

To get headers and status returned from the handler, we can access `set` from the context.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.onAfterResponse(({ set }) => {
		console.log(set.status, set.headers)
	})
	.get('/', () => 'Hello')
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/tutorial/patterns/macro.md'
---

# Macro

Reusable route options.

Imagine we have an authentication check like this:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/user', ({ body }) => body, {
		cookie: t.Object({
			session: t.String()
		}),
		beforeHandle({ cookie: { session } }) {
			if(!session.value) throw 'Unauthorized'
		}
	})
	.listen(3000)
```

If we have multiple routes that require authentication, we have to repeat the same options over and over again.

Instead, we can use a macro to reuse route options:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.macro('auth', {
		cookie: t.Object({
			session: t.String()
		}),
		// psuedo auth check
		beforeHandle({ cookie: { session }, status }) {
			if(!session.value) return status(401)
		}
	})
	.post('/user', ({ body }) => body, {
		auth: true // [!code ++]
	})
	.listen(3000)
```

**auth** will then inline both **cookie**, and **beforeHandle** to the route.

Simply put, Macro **is a reusable route option**, similar to function but as a route option with **type soundness**.

## Assignment

Let's define a macro to check if a body is a Fibonacci number:

```typescript
function isFibonacci(n: number) {
	let a = 0, b = 1
	while(b < n) [a, b] = [b, a + b]
	return b === n || n === 0
}
```

\<template #answer>

1. To enforce type, we can define a `body` property in the macro.
2. To short-circuit the request, we can use `status` function to return early.

```typescript
import { Elysia, t } from 'elysia'

function isPerfectSquare(x: number) {
    const s = Math.floor(Math.sqrt(x))
    return s * s === x
}

function isFibonacci(n: number) {
    if (n < 0) return false

    return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4)
}

new Elysia()
    .macro('isFibonacci', {
		body: t.Number(),
        beforeHandle({ body, status }) {
            if(!isFibonacci(body)) return status(418)
        }
    })
	.post('/', ({ body }) => body, {
		isFibonacci: true
	})
    .listen(3000)
```

---

---
url: 'https://elysiajs.com/patterns/macro.md'
---

# Macro&#x20;

Macro is similar to a function that has control over the lifecycle event, schema, and context with full type safety.

Once defined, it will be available in the hook and can be activated by adding the property.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia({ name: 'plugin' })
    .macro({
        hi: (word: string) => ({
            beforeHandle() {
                console.log(word)
            }
        })
    })

const app = new Elysia()
    .use(plugin)
    .get('/', () => 'hi', {
        hi: 'Elysia' // [!code ++]
    })
```

Accessing the path should log **"Elysia"** as a result.

## Property shorthand

Starting from Elysia 1.2.10, each property in the macro object can be a function or an object.

If the property is an object, it will be translated to a function that accepts a boolean parameter and will be executed if the parameter is true.

```typescript
import { Elysia } from 'elysia'

export const auth = new Elysia()
    .macro({
    	// This property shorthand
    	isAuth: { // [!code ++]
      		resolve: () => ({ // [!code ++]
      			user: 'saltyaom' // [!code ++]
      		}) // [!code ++]
        }, // [!code ++]
        // is equivalent to
        isAuth(enabled: boolean) { // [!code --]
        	if(!enabled) return // [!code --]
// [!code --]

        	return { // [!code --]
				resolve() { // [!code --]
					return { // [!code --]
						user // [!code --]
					} // [!code --]
				} // [!code --]
         	} // [!code --]
        } // [!code --]
    })
```

## Error handling

You can return an error HTTP status by returning a `status`.

```ts
import { Elysia, status } from 'elysia' // [!code ++]

new Elysia()
	.macro({
		auth: {
			resolve({ headers }) {
				if(!headers.authorization)
					return status(401, 'Unauthorized') // [!code ++]
		
				return {
					user: 'SaltyAom'
				}
			}
		}
	})
	.get('/', ({ user }) => `Hello ${user}`, {
	            // ^?
		auth: true
	})
```

It's recommended that you `return status` instead of `throw new Error()` to annotate correct HTTP status code.

If you throw an error instead, Elysia will convert it to `500 Internal Server Error` by default.

It's also recommended to use `return status` instead of `throw status` to ensure type inference for both [Eden](/eden/overview) and [OpenAPI Type Gen](/patterns/openapi#openapi-from-types).

## Resolve

You can add a property to the context by returning an object with a [**resolve**](/essential/life-cycle.html#resolve) function.

```ts twoslash
import { Elysia } from 'elysia'

new Elysia()
	.macro({
		user: (enabled: true) => ({
			resolve: () => ({
				user: 'Pardofelis'
			})
		})
	})
	.get('/', ({ user }) => user, {
                          // ^?
		user: true
	})
```

In the example above, we add a new property **user** to the context by returning an object with a **resolve** function.

Here's an example where macro resolve could be useful:

* perform authentication and add the user to the context
* run an additional database query and add data to the context
* add a new property to the context

### Macro extension with resolve

Due to TypeScript's limitation, a macro that extends other macro cannot infer type into **resolve** function.

We provide a named single macro as a workaround to this limitation.

```typescript twoslash
import { Elysia, t } from 'elysia'
new Elysia()
	.macro('user', {
		resolve: () => ({
			user: 'lilith' as const
		})
	})
	.macro('user2', {
		user: true,
		resolve: ({ user }) => {
		//           ^?
		}
	})
```

## Schema

You can define a custom schema for your macro to ensure that the route using the macro is passing the correct types.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.macro({
		withFriends: {
			body: t.Object({
				friends: t.Tuple([t.Literal('Fouco'), t.Literal('Sartre')])
			})
		}
	})
	.post('/', ({ body }) => body.friends, {
//                                  ^?

		body: t.Object({
			name: t.Literal('Lilith')
		}),
		withFriends: true
	})
```

Macro with schema will automatically validate and infer types to ensure type safety, and it can co-exist with existing schema as well.

You can also stack multiple schemas from different macros, or even from the Standard Validator, and it will work together seamlessly.

### Schema with lifecycle in the same macro

Similar to [Macro extension with resolve](#macro-extension-with-resolve),

Macro schema also supports type inference for **lifecycle within the same macro** **BUT** only with a named single macro due to TypeScript limitation.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.macro('withFriends', {
		body: t.Object({
			friends: t.Tuple([t.Literal('Fouco'), t.Literal('Sartre')])
		}),
		beforeHandle({ body: { friends } }) {
//                             ^?
		}
	})
```

If you want to use lifecycle type inference within the same macro, you might want to use a named single macro instead of multiple stacked macros

> Not to be confused with using macro schema to infer type into the route's lifecycle event. That works just fine. This limitation only applies to using lifecycle within the same macro.

## Extension

Macro can extend other macros, allowing you to build upon an existing one.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.macro({
		sartre: {
			body: t.Object({
				sartre: t.Literal('Sartre')
			})
		},
		fouco: {
			body: t.Object({
				fouco: t.Literal('Fouco')
			})
		},
		lilith: {
			fouco: true,
			sartre: true,
			body: t.Object({
				lilith: t.Literal('Lilith')
			})
		}
	})
	.post('/', ({ body }) => body, {
//                            ^?
		lilith: true
	})



// ---cut-after---
//
```

This allows you to build upon existing macro, and add more functionality to it.

## Deduplication

Macro will automatically deduplicate the lifecycle event, ensuring that each lifecycle event is only executed once.

By default, Elysia will use the property value as the seed, but you can override it by providing a custom seed.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.macro({
		sartre: (role: string) => ({
			seed: role, // [!code ++]
			body: t.Object({
				sartre: t.Literal('Sartre')
			})
		})
	})
```

However, if you ever accidentally create a circular dependency, Elysia has a limited stack of 16 to prevent an infinite loop in both runtime and type inference.

If the route already has OpenAPI detail, it will merge the details together but prefers the route detail over macro detail.

---

---
url: 'https://elysiajs.com/tutorial/features/mount.md'
---

# Mount

Elysia provides a Elysia.mount to interoperate between backend frameworks that is built on Web Standard like Hono, H3, etc.

```typescript
import { Elysia, t } from 'elysia'
import { Hono } from 'hono'

const hono = new Hono()
	.get('/', (c) => c.text('Hello from Hono'))

new Elysia()
	.get('/', 'Hello from Elysia')
	.mount('/hono', hono.fetch)
	.listen(3000)
```

This allows us to gradually migrate our application to Elysia, or use multiple frameworks in a single application.

## Assignment

Let's use the preview to **GET '/hono'** to see if our Hono route is working.

Try to modify the code and see how it changes!

---

---
url: 'https://elysiajs.com/patterns/mount.md'
---

# Mount&#x20;

[WinterTC](https://wintertc.org/) is a standard for building HTTP Server behind Cloudflare, Deno, Vercel, and others.

It allows web servers to run interoperably across runtimes by using [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request), and [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response).

Elysia is WinterTC compliant. Optimized to run on Bun, but also supports other runtimes if possible.

This allows any WinterTC-compliant framework or code to run together, allowing frameworks like Elysia, Hono, Remix, Itty Router to run together in a simple function.

## Mount

To use **.mount**, [simply pass a `fetch` function](https://twitter.com/saltyAom/status/1684786233594290176):

```ts
import { Elysia } from 'elysia'
import { Hono } from 'hono'

const hono = new Hono()
	.get('/', (c) => c.text('Hello from Hono!'))

const app = new Elysia()
    .get('/', () => 'Hello from Elysia')
    .mount('/hono', hono.fetch)
```

Any framework that uses `Request` and `Response` can interoperate with Elysia like

* Hono
* Nitro
* H3
* [Nextjs API Route](/integrations/nextjs)
* [Nuxt API Route](/integrations/nuxt)
* [SvelteKit API Route](/integrations/sveltekit)

And these can be use on multiple runtimes like:

* Bun
* Deno
* Vercel Edge Runtime
* Cloudflare Worker
* Netlify Edge Function

If the framework supports the **.mount** function, you can also mount Elysia inside another framework:

```ts
import { Elysia } from 'elysia'
import { Hono } from 'hono'

const elysia = new Elysia()
    .get('/', () => 'Hello from Elysia inside Hono inside Elysia')

const hono = new Hono()
    .get('/', (c) => c.text('Hello from Hono!'))
    .mount('/elysia', elysia.fetch)

const main = new Elysia()
    .get('/', () => 'Hello from Elysia')
    .mount('/hono', hono.fetch)
    .listen(3000)
```

This makes the possibility of an interoperable framework and runtime a reality.

---

---
url: 'https://elysiajs.com/tutorial/features/openapi.md'
---

# OpenAPI

Elysia is built around OpenAPI, and supports OpenAPI documentation out of the box.

We can use OpenAPI plugin to show an API documentation.

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi' // [!code ++]

new Elysia()
	.use(openapi()) // [!code ++]
	.post(
		'/',
		({ body }) => body,
		{
			body: t.Object({
				age: t.Number()
			})
		}
	)
	.listen(3000)
```

Once added, we can access our API documentation at **/openapi**.

## Detail

We can provide API documentation with a `detail` field which follows OpenAPI 3.0 specification (with auto-completion):

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
	.use(openapi())
	.post(
		'/',
		({ body }) => body,
		{
			body: t.Object({
				age: t.Number()
			}),
			detail: { // [!code ++]
				summary: 'Create a user', // [!code ++]
				description: 'Create a user with age', // [!code ++]
				tags: ['User'], // [!code ++]
			} // [!code ++]
		}
	)
	.listen(3000)
```

## Reference Model

We can also define reusable schema with Reference Model:

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
	.use(openapi())
	.model({
		age: t.Object({ // [!code ++]
			age: t.Number() // [!code ++]
		}) // [!code ++]
	})
	.post(
		'/',
		({ body }) => body,
		{
			age: t.Object({ // [!code --]
				age: t.Number() // [!code --]
			}), // [!code --]
			body: 'age',  // [!code ++]
			detail: {
				summary: 'Create a user',
				description: 'Create a user with age',
				tags: ['User'],
			}
		}
	)
	.listen(3000)
```

When we defined a reference model, it will be shown in the **Components** section of the OpenAPI documentation.

## Type Gen

OpenAPI Type Gen can document your API **without manual annotation** infers directly from TypeScript type. No Zod, TypeBox, manual interface declaraiont, etc.

**This feature is unique to Elysia**, and is not available in other JavaScript frameworks.

For example, if you use Drizzle ORM or Prisma, Elysia can infer the schema directly from the query.

![Drizzle](/blog/openapi-type-gen/drizzle-typegen.webp)

> Returning Drizzle query from Elysia route handler will be automatically inferred into OpenAPI schema.

To use OpenAPI Type Gen, simply apply the `fromTypes` plugin before `openapi` plugin.

```typescript
import { Elysia } from 'elysia'

import { openapi, fromTypes } from '@elysia/openapi' // [!code ++]

new Elysia()
	.use(openapi({
		references: fromTypes() // [!code ++]
	}))
	.get('/', { hello: 'world' })
	.listen(3000)
```

### Browser Environment

Unfortunately, this feature requires the **fs** module to read your source code, and is not available in this web playground. As Elysia is running directly in your browser (not a separated server).

You can try this feature locally with Type Gen Example repository:

```bash
git clone https://github.com/SaltyAom/elysia-typegen-example && \
cd elysia-typegen-example && \
bun install && \
bun run dev
```

## Assignment

Let's use the preview to **GET '/openapi'** and see how our API documentation looks.

This API documentation is reflected from your code.

Try to modify the code and see how the documentation changes!

---

---
url: 'https://elysiajs.com/patterns/openapi.md'
---

# OpenAPI&#x20;

Elysia has first-class support and follows OpenAPI schema by default.

Elysia can automatically generate an API documentation page by using an OpenAPI plugin.

To generate the Swagger page, install the plugin:

```bash
bun add @elysia/openapi
```

And register the plugin to the server:

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi' // [!code ++]

new Elysia()
	.use(openapi()) // [!code ++]
```

Accessing `/openapi` would show you a Scalar UI with the generated endpoint documentation from the Elysia server.

For OpenAPI plugin configuration, see the [OpenAPI plugin page](/plugins/openapi).

## OpenAPI from types

> This is optional, but we highly recommend it for much better documentation experience.

By default, Elysia relies on runtime schema to generate OpenAPI documentation.

However, you can also generate OpenAPI documentation from types by using a generator from OpenAPI plugin as follows:

1. Specify your Elysia root file (if not specified, Elysia will use `src/index.ts`), and export an instance

2. Import a generator and provide a **file path from project root** to type generator

```ts
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi' // [!code ++]

export const app = new Elysia() // [!code ++]
    .use(
        openapi({
            references: fromTypes() // [!code ++]
        })
    )
    .get('/', { test: 'hello' as const })
    .post('/json', ({ body, status }) => body, {
        body: t.Object({
            hello: t.String()
        })
    })
    .listen(3000)
```

Elysia will attempt to generate OpenAPI documentation by reading the type of an exported instance to generate OpenAPI documentation.

This will co-exists with the runtime schema, and the runtime schema will take precedence over the type definition.

### Production

In production environment, it's likely that you might compile Elysia to a [single executable with Bun](/patterns/deploy.html) or [bundle into a single JavaScript file](https://elysiajs.com/patterns/deploy.html#compile-to-javascript).

It's recommended that you should pre-generate the declaration file (**.d.ts**) to provide type declaration to the generator.

```ts
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi'

const app = new Elysia()
    .use(
        openapi({
            references: fromTypes(
            	process.env.NODE_ENV === 'production' // [!code ++]
             		? 'dist/index.d.ts' // [!code ++]
               		: 'src/index.ts' // [!code ++]
            )
        })
    )
```

### Caveat: Explicit types

OpenAPI Type Gen works best when using implicit types.

Sometimes, explicit types may cause an issue for the generator being unable to resolve properly.

In this case, you can use `Prettify` to inline the type:

```ts
import { Elysia, t } from 'elysia'

// Your custom type
interface User {
	id: number
	name: string
}

// Type helper to inline the type
type Prettify<T> = { // [!code ++]
	[K in keyof T]: T[K] // [!code ++]
} & {} // [!code ++]

// Add Prettify to inline the type
function getUser(): Prettify<User> { // [!code ++]
	// Your logic to get user // [!code ++]
} // [!code ++]
```

This should fix when type not showing up.

### Caveat: Root path

As it's unreliable to guess to root of the project, it's recommended to provide the path to the project root to allow generator to run correctly, especially when using monorepo.

```ts
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi'

export const app = new Elysia()
    .use(
        openapi({
            references: fromTypes('src/index.ts', {
            	projectRoot: path.join('..', import.meta.dir) // [!code ++]
            })
        })
    )
    .get('/', { test: 'hello' as const })
    .post('/json', ({ body, status }) => body, {
        body: t.Object({
            hello: t.String()
        })
    })
    .listen(3000)
```

### Custom tsconfig.json

If you have multiple `tsconfig.json` files, it's important that you must specify a correct `tsconfig.json` file to be used for type generation.

```ts
import { Elysia, t } from 'elysia'
import { openapi, fromTypes } from '@elysia/openapi'

export const app = new Elysia()
    .use(
        openapi({
            references: fromTypes('src/index.ts', {
            	// This is reference from root of the project
            	tsconfigPath: 'tsconfig.dts.json' // [!code ++]
            })
        })
    )
    .get('/', { test: 'hello' as const })
    .post('/json', ({ body, status }) => body, {
        body: t.Object({
            hello: t.String()
        })
    })
    .listen(3000)
```

## Standard Schema with OpenAPI

Elysia will try to use a native method from each schema to convert to OpenAPI schema.

However, if the schema doesn't provide a native method, you can provide a custom schema to OpenAPI by providing a `mapJsonSchema` as follows:

\<Tab
id="schema-openapi"
noTitle
:names="\['Zod', 'Valibot', 'Effect']"
:tabs="\['zod', 'valibot', 'effect']"

>

### Zod OpenAPI

As Zod doesn't have a `toJSONSchema` method on the schema, we need to provide a custom mapper to convert Zod schema to OpenAPI schema.

::: code-group

```typescript [Zod 4]
import openapi from '@elysia/openapi'
import * as z from 'zod'

openapi({
	mapJsonSchema: {
		zod: z.toJSONSchema
	}
})
```

```typescript [Zod 3]
import openapi from '@elysia/openapi'
import { zodToJsonSchema } from 'zod-to-json-schema'

openapi({
	mapJsonSchema: {
		zod: zodToJsonSchema
	}
})
```

:::

### Valibot OpenAPI

Valibot use a separate package (`@valibot/to-json-schema`) to convert Valibot schema to JSON Schema.

```typescript
import openapi from '@elysia/openapi'
import { toJsonSchema } from '@valibot/to-json-schema'

openapi({
	mapJsonSchema: {
		valibot: toJsonSchema
	}
})
```

### Effect OpenAPI

As Effect doesn't have a `toJSONSchema` method on the schema, we need to provide a custom mapper to convert Effect schema to OpenAPI schema.

```typescript
import openapi from '@elysia/openapi'
import { JSONSchema } from 'effect'

openapi({
 	mapJsonSchema: {
   		effect: JSONSchema.make
 	}
})
```

## Describing routes

We can add route information by providing a schema type.

However, sometimes defining only a type does not make it clear what the route might do. You can use [detail](/plugins/openapi#detail) fields to explicitly describe the route.

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
	.use(openapi())
	.post(
		'/sign-in',
		({ body }) => body, {
    		body: t.Object(
      		{
	            username: t.String(),
	            password: t.String({
	                minLength: 8,
	                description: 'User password (at least 8 characters)' // [!code ++]
	            })
	        },
	        { // [!code ++]
	            description: 'Expected a username and password' // [!code ++]
	        } // [!code ++]
	    ),
	    detail: { // [!code ++]
	        summary: 'Sign in the user', // [!code ++]
	        tags: ['authentication'] // [!code ++]
	    } // [!code ++]
	})
```

The detail fields follows an OpenAPI V3 definition with auto-completion and type-safety by default.

Detail is then passed to OpenAPI to put the description to OpenAPI route.

## Response headers

We can add response headers by wrapping a schema with `withHeader`:

```typescript
import { Elysia, t } from 'elysia'
import { openapi, withHeader } from '@elysia/openapi' // [!code ++]

new Elysia()
	.use(openapi())
	.get(
		'/thing',
		({ body, set }) => {
			set.headers['x-powered-by'] = 'Elysia'

			return body
		},
		{
		    response: withHeader( // [!code ++]
				t.Literal('Hi'), // [!code ++]
				{ // [!code ++]
					'x-powered-by': t.Literal('Elysia') // [!code ++]
				} // [!code ++]
			) // [!code ++]
		}
	)
```

Note that `withHeader` is an annotation only, and does not enforce or validate the actual response headers. You need to set the headers manually.

### Hide route

You can hide the route from the Swagger page by setting `detail.hide` to `true`

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
	.use(openapi())
	.post(
		'/sign-in',
		({ body }) => body,
		{
		    body: t.Object(
		        {
		            username: t.String(),
		            password: t.String()
		        },
		        {
		            description: 'Expected a username and password'
		        }
		    ),
		    detail: { // [!code ++]
		        hide: true // [!code ++]
		    } // [!code ++]
		}
	)
```

## Tags

Elysia can separate the endpoints into groups by using the Swagger tag system

Firstly define the available tags in the Swagger config object

```typescript
new Elysia().use(
    openapi({
        documentation: {
            tags: [
                { name: 'App', description: 'General endpoints' },
                { name: 'Auth', description: 'Authentication endpoints' }
            ]
        }
    })
)
```

Then use the detail property of the endpoint configuration section to assign that endpoint to the group

```typescript
new Elysia()
    .get('/', () => 'Hello Elysia', {
        detail: {
            tags: ['App']
        }
    })
    .group('/auth', (app) =>
        app.post(
            '/sign-up',
            ({ body }) =>
                db.user.create({
                    data: body,
                    select: {
                        id: true,
                        username: true
                    }
                }),
            {
                detail: {
                    tags: ['Auth']
                }
            }
        )
    )
```

This will produce a Swagger page as follows


### Tags group

Elysia may accept tags to add an entire instance or group of routes to a specific tag.

```typescript
import { Elysia, t } from 'elysia'

new Elysia({
    tags: ['user']
})
    .get('/user', 'user')
    .get('/admin', 'admin')
```

## Models

By using [reference model](/essential/validation.html#reference-model), Elysia will handle the schema generation automatically.

By separating models into a dedicated section and linked by reference.

```typescript
new Elysia()
    .model({
        User: t.Object({
            id: t.Number(),
            username: t.String()
        })
    })
    .get('/user', () => ({ id: 1, username: 'saltyaom' }), {
        response: {
            200: 'User'
        },
        detail: {
            tags: ['User']
        }
    })
```

## Guard

Alternatively, Elysia may accept guards to add an entire instance or group of routes to a specific guard.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .guard({
        detail: {
            description: 'Require user to be logged in'
        }
    })
    .get('/user', 'user')
    .get('/admin', 'admin')
```

## Change OpenAPI Endpoint

You can change the OpenAPI endpoint by setting [path](#path) in the plugin config.

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
    .use(
        openapi({
            path: '/v2/openapi'
        })
    )
    .listen(3000)
```

## Customize OpenAPI info

We can customize the OpenAPI information by setting [documentation.info](#documentationinfo) in the plugin config.

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
    .use(
        openapi({
            documentation: {
                info: {
                    title: 'Elysia Documentation',
                    version: '1.0.0'
                }
            }
        })
    )
    .listen(3000)
```

This can be useful for

* adding a title
* setting an API version
* adding a description explaining what our API is about
* explaining what tags are available, what each tag means

## Security Configuration

To secure your API endpoints, you can define security schemes in the Swagger configuration. The example below demonstrates how to use Bearer Authentication (JWT) to protect your endpoints:

```typescript
new Elysia().use(
    openapi({
        documentation: {
            components: {
                securitySchemes: {
                    bearerAuth: {
                        type: 'http',
                        scheme: 'bearer',
                        bearerFormat: 'JWT'
                    }
                }
            }
        }
    })
)

export const addressController = new Elysia({
    prefix: '/address',
    detail: {
        tags: ['Address'],
        security: [
            {
                bearerAuth: []
            }
        ]
    }
})
```

This will ensure that all endpoints under the `/address` prefix require a valid JWT token for access.

---

---
url: 'https://elysiajs.com/plugins/openapi.md'
---

# OpenAPI Plugin&#x20;

Plugin for [elysia](https://github.com/elysiajs/elysia) to auto-generate API documentation page.

Install with:

```bash
bun add @elysia/openapi
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
    .use(openapi())
    .get('/', () => 'hello')
    .post('/hello', () => 'OpenAPI')
    .listen(3000)
```

Accessing `/openapi` would show you a Scalar UI with the generated endpoint documentation from the Elysia server. You can also access the raw OpenAPI spec at `/openapi/json`.

::: tip
This page is the plugin configuration reference.

If you're looking for common patterns or advanced usage of OpenAPI, check out [Patterns: OpenAPI](/patterns/openapi)
:::

## Detail

`detail` extends the [OpenAPI Operation Object](https://spec.openapis.org/oas/v3.0.3.html#operation-object)

The detail field is an object that can be used to describe information about the route for API documentation.

It may contain the following fields:

## detail.hide

You can hide the route from the Swagger page by setting `detail.hide` to `true`

```typescript
import { Elysia, t } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia().use(openapi()).post('/sign-in', ({ body }) => body, {
    body: t.Object(
        {
            username: t.String(),
            password: t.String()
        },
        {
            description: 'Expected a username and password'
        }
    ),
    detail: {
        // [!code ++]
        hide: true // [!code ++]
    } // [!code ++]
})
```

### detail.deprecated

Declares this operation to be deprecated. Consumers SHOULD refrain from usage of the declared operation. Default value is `false`.

### detail.description

A verbose explanation of the operation behavior.

### detail.summary

A short summary of what the operation does.

## Config

Below is the config that is accepted by the plugin

## enabled

@default true
Enable/Disable the plugin

## documentation

OpenAPI documentation information

@see https://spec.openapis.org/oas/v3.0.3.html

## exclude

Configuration to exclude paths or methods from documentation

## exclude.methods

List of methods to exclude from documentation

## exclude.paths

List of paths to exclude from documentation

## exclude.staticFile

@default true

Exclude static file routes from documentation

## exclude.tags

List of tags to exclude from documentation

## mapJsonSchema

A custom mapping function from standard schema to OpenAPI schema

### Example

```typescript
import { openapi } from '@elysia/openapi'
import { toJsonSchema } from '@valibot/to-json-schema'

openapi({
	mapJsonSchema: {
	  	valibot: toJsonSchema
  	}
})
```

## path

@default '/openapi'

The endpoint to expose OpenAPI documentation frontend

## provider

@default 'scalar'

OpenAPI documentation frontend provider between:

* [Scalar](https://github.com/scalar/scalar)
* [SwaggerUI](https://github.com/swagger-api/swagger-ui)
* null: disable frontend

## references

Additional OpenAPI reference for each endpoint

## scalar

Scalar configuration, refers to [Scalar config](https://github.com/scalar/scalar/blob/main/documentation/configuration.md)

### Self-hosted Scalar bundle

Self-host the Scalar bundle and disable CDN Fonts.

Note: `cdn` is an Elysia OpenAPI plugin option (not part of Scalar’s own config); it overrides the URI to the Scalar bundle.

```typescript
    openapi({ 
      scalar: {
        cdn: "/public/scalar-standalone.min.js", // plugin override for Scalar bundle URI (self-hosted)
        withDefaultFonts: false, // disable Scalar’s default font CDN
      },
    })
```

## specPath

@default '/${path}/json'

The endpoint to expose OpenAPI specification in JSON format

## swagger

Swagger config, refers to [Swagger config](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)

Below you can find common patterns to use the plugin.

---

---
url: 'https://elysiajs.com/patterns/opentelemetry.md'
---

# OpenTelemetry

To start using OpenTelemetry, install `@elysia/opentelemetry` and apply plugin to any instance.

```typescript
import { Elysia } from 'elysia'
import { opentelemetry } from '@elysia/opentelemetry'

new Elysia()
	.use(opentelemetry())
```

![OpenTelemetry visualize via Axiom](/assets/axiom.webp)

Why use OpenTelemetry with Elysia?

* 1 line config
* Span name is the function name
* Grouping relevant lifecycle together
* Wrap code to record a specific part
* Support Server-Sent Event, and response streaming
* Compatible with any OpenTelemetry compatible library

You may export telemetry data to Jaeger, Zipkin, New Relic, Axiom or any other OpenTelemetry compatible backend.

### Export OpenTelemetry data

We can export OpenTelemetry data to any backend that supports OpenTelemetry protocol.

Here's an example of exporting telemetry to [Axiom](https://axiom.co)

```typescript
import { Elysia } from 'elysia'
import { opentelemetry } from '@elysia/opentelemetry'

import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto'

new Elysia().use(
	opentelemetry({
		spanProcessors: [
			new BatchSpanProcessor(
				new OTLPTraceExporter({
					url: 'https://api.axiom.co/v1/traces', // [!code ++]
					headers: {
						// [!code ++]
						Authorization: `Bearer ${Bun.env.AXIOM_TOKEN}`, // [!code ++]
						'X-Axiom-Dataset': Bun.env.AXIOM_DATASET // [!code ++]
					} // [!code ++]
				})
			)
		]
	})
)
```

## OpenTelemetry SDK

Elysia OpenTelemetry is for applying OpenTelemetry to Elysia server only.

You may use OpenTelemetry SDK normally, and the span is run under Elysia's request span, it will automatically appear in Elysia trace.

However, we also provide a `getTracer`, and `record` utility to collect span from any part of your application.

```typescript
import { Elysia } from 'elysia'
import { record } from '@elysia/opentelemetry'

export const plugin = new Elysia().get('', () => {
	return record('database.query', () => {
		return db.query('SELECT * FROM users')
	})
})
```

## Record utility

`record` is equivalent to OpenTelemetry's `startActiveSpan` but it will handle auto-closing and capture exception automatically.

You may think of `record` as a label for your code that will be shown in trace.

### Prepare your codebase for observability

Elysia OpenTelemetry will group lifecycle and read the **function name** of each hook as the name of the span.

It's a good time to **name your function**.

If your hook handler is an arrow function, you may refactor it to named function to understand the trace better, otherwise your trace span will be named as `anonymous`.

```typescript
const bad = new Elysia()
	// ⚠️ span name will be anonymous
	.derive(async ({ cookie: { session } }) => {
		return {
			user: await getProfile(session)
		}
	})

const good = new Elysia()
	// ✅ span name will be getProfile
	.derive(async function getProfile({ cookie: { session } }) {
		return {
			user: await getProfile(session)
		}
	})
```

## getCurrentSpan

`getCurrentSpan` is a utility to get the current span of the current request when you are outside of the handler.

```typescript
import { getCurrentSpan } from '@elysia/opentelemetry'

function utility() {
	const span = getCurrentSpan()
	span.setAttributes({
		'custom.attribute': 'value'
	})
}
```

This works outside of the handler by retrieving current span from `AsyncLocalStorage`

## setAttributes

`setAttributes` is a utility to set attributes to the current span.

```typescript
import { setAttributes } from '@elysia/opentelemetry'

function utility() {
	setAttributes({
		'custom.attribute': 'value'
	})
}
```

This is a syntax sugar for `getCurrentSpan().setAttributes`

## Configuration

See [opentelemetry plugin](/plugins/opentelemetry) for configuration option and definition.

## Instrumentations Advanced Concept

Many instrumentation libraries required that the SDK **MUST** run before importing the module.

For example, to use `PgInstrumentation`, the `OpenTelemetry SDK` must run before importing the `pg` module.

To achieve this in Bun, we can

1. Separate an OpenTelemetry setup into a different file
2. create `bunfig.toml` to preload the OpenTelemetry setup file

Let's create a new file in `src/instrumentation.ts`

```ts [src/instrumentation.ts]
import { opentelemetry } from '@elysia/opentelemetry'
import { PgInstrumentation } from '@opentelemetry/instrumentation-pg'

export const instrumentation = opentelemetry({
	instrumentations: [new PgInstrumentation()]
})
```

Then we can apply this `instrumentaiton` plugin into our main instance in `src/index.ts`

```ts [src/index.ts]
import { Elysia } from 'elysia'
import { instrumentation } from './instrumentation.ts'

new Elysia().use(instrumentation).listen(3000)
```

Then create a `bunfig.toml` with the following:

```toml [bunfig.toml]
preload = ["./src/instrumentation.ts"]
```

This will tell Bun to load and setup `instrumentation` before running the `src/index.ts` allowing OpenTelemetry to do its setup as needed.

### Deploying to production Advanced Concept

If you are using `bun build` or other bundlers.

As OpenTelemetry relies on monkey-patching `node_modules/<library>`. It's required to make instrumentations work properly, we need to specify libraries to be instrumented as an external module to exclude it from being bundled.

For example, if you are using `@opentelemetry/instrumentation-pg` to instrument `pg` library. We need to exclude `pg` from being bundled and make sure that it is importing `node_modules/pg`.

To make this work, we may specify `pg` as an external module with `--external pg`

```bash
bun build --compile --external pg --outfile server src/index.ts
```

This tells bun not to bundle `pg` into the final output file, and will be imported from the **node\_modules** directory at runtime. So on a production server, you must also keep the **node\_modules** directory.

It's recommended to specify packages that should be available in a production server as **dependencies** in **package.json** and use `bun install --production` to install only production dependencies.

```json
{
	"dependencies": {
		"pg": "^8.15.6"
	},
	"devDependencies": {
		"@elysia/opentelemetry": "^1.2.0",
		"@opentelemetry/instrumentation-pg": "^0.52.0",
		"@types/pg": "^8.11.14",
		"elysia": "^1.2.25"
	}
}
```

Then after running a build command, on a production server

```bash
bun install --production
```

If the node\_modules directory still includes development dependencies, you may remove the node\_modules directory and reinstall production dependencies again.

---

---
url: 'https://elysiajs.com/plugins/opentelemetry.md'
---

# OpenTelemetry

::: tip
This page is a **config reference** for **OpenTelemetry**. If you're looking to set up and integrate with OpenTelemetry, we recommend taking a look at [Integrate with OpenTelemetry](/patterns/opentelemetry) instead.
:::

To start using OpenTelemetry, install `@elysia/opentelemetry` and apply plugin to any instance.

```typescript
import { Elysia } from 'elysia'
import { opentelemetry } from '@elysia/opentelemetry'

import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto'

new Elysia()
	.use(
		opentelemetry({
			spanProcessors: [
				new BatchSpanProcessor(
					new OTLPTraceExporter()
				)
			]
		})
	)
```

![jaeger showing collected trace automatically](/blog/elysia-11/jaeger.webp)

Elysia OpenTelemetry will **collect spans from any library compatible with the OpenTelemetry standard**, and will apply parent and child span automatically.

## Usage

See [opentelemetry](/patterns/opentelemetry) for usage and utilities

## Config

This plugin extends OpenTelemetry SDK parameters options.

Below is a config which is accepted by the plugin

### autoDetectResources - boolean

Detect resources automatically from the environment using the default resource detectors.

default: `true`

### contextManager - ContextManager

Use a custom context manager.

default: `AsyncHooksContextManager`

### textMapPropagator - TextMapPropagator

Use a custom propagator.

default: `CompositePropagator` using W3C Trace Context and Baggage

### metricReader - MetricReader

Add a MetricReader that will be passed to the MeterProvider.

### views - View\[]

A list of views to be passed to the MeterProvider.

Accepts an array of View-instances. This parameter can be used to configure explicit bucket sizes of histogram metrics.

### instrumentations - (Instrumentation | Instrumentation\[])\[]

Configure instrumentations.

By default `getNodeAutoInstrumentations` is enabled, if you want to enable them you can use either metapackage or configure each instrumentation individually.

default: `getNodeAutoInstrumentations()`

### resource - IResource

Configure a resource.

Resources may also be detected by using the autoDetectResources method of the SDK.

### resourceDetectors - Array\<Detector | DetectorSync>

Configure resource detectors. By default, the resource detectors are \[envDetector, processDetector, hostDetector]. NOTE: In order to enable the detection, the parameter autoDetectResources has to be true.

If resourceDetectors was not set, you can also use the environment variable OTEL\_NODE\_RESOURCE\_DETECTORS to enable only certain detectors, or completely disable them:

* env
* host
* os
* process
* serviceinstance (experimental)
* all - enable all resource detectors above
* none - disable resource detection

For example, to enable only the env, host detectors:

```bash
export OTEL_NODE_RESOURCE_DETECTORS="env,host"
```

### sampler - Sampler

Configure a custom sampler. By default, all traces will be sampled.

### serviceName - string

Namespace to be identified as.

### spanProcessors - SpanProcessor\[]

An array of span processors to register to the tracer provider.

### traceExporter - SpanExporter

Configure a trace exporter. If an exporter is configured, it will be used with a `BatchSpanProcessor`.

If an exporter OR span processor is not configured programmatically, this package will auto setup the default otlp exporter with http/protobuf protocol with a BatchSpanProcessor.

### spanLimits - SpanLimits

Configure tracing parameters. These are the same trace parameters used to configure a tracer.

---

---
url: 'https://elysiajs.com/eden/treaty/overview.md'
---

# Eden Treaty

Eden Treaty is an object representation used to interact with a server and features type safety, auto-completion, and error handling.

To use Eden Treaty, first export your existing Elysia server's type:

```typescript
// server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/hi', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]
```

Then import the server type and consume the Elysia API on the client:

```typescript twoslash
// @filename: server.ts
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .get('/hi', () => 'Hi Elysia')
    .get('/id/:id', ({ params: { id } }) => id)
    .post('/mirror', ({ body }) => body, {
        body: t.Object({
            id: t.Number(),
            name: t.String()
        })
    })
    .listen(3000)

export type App = typeof app // [!code ++]

// @filename: client.ts
// ---cut---
// client.ts
import { treaty } from '@elysia/eden'
import type { App } from './server' // [!code ++]

const app = treaty<App>('localhost:3000')

// response type: 'Hi Elysia'
const { data, error } = await app.hi.get()
      // ^?
```

## Tree-like syntax

HTTP Path is a resource indicator for a file system tree.

A file system consists of multiple levels of folders, for example:

* /documents/elysia
* /documents/kalpas
* /documents/kelvin

Each level is separated by **/** (slash) and a name.

However, in JavaScript, instead of using **"/"** (slash), we use **"."** (dot) to access deeper resources.

Eden Treaty turns an Elysia server into a tree-like file system that can be accessed from the JavaScript frontend instead.

| Path         | Treaty       |
| ------------ | ------------ |
| /            |              |
| /hi          | .hi          |
| /deep/nested | .deep.nested |

Combined with the HTTP method, we can interact with the Elysia server.

| Path         | Method | Treaty              |
| ------------ | ------ | ------------------- |
| /            | GET    | .get()              |
| /hi          | GET    | .hi.get()           |
| /deep/nested | GET    | .deep.nested.get()  |
| /deep/nested | POST   | .deep.nested.post() |

## Dynamic path

However, dynamic path parameters cannot be expressed using notation alone. If they are fully replaced, we don't know what the parameter name is supposed to be.

```typescript
// ❌ Unclear what the value is supposed to represent?
treaty.item['skadi'].get()
```

To handle this, we can specify a dynamic path using a function to provide a key value instead.

```typescript
// ✅ Clear that the value is dynamic and the path is 'name'
treaty.item({ name: 'Skadi' }).get()
```

| Path            | Treaty                           |
| --------------- | -------------------------------- |
| /item           | .item                            |
| /item/:name     | .item({ name: 'Skadi' })         |
| /item/:name/id  | .item({ name: 'Skadi' }).id      |

---

---
url: 'https://elysiajs.com/playground.md'
---

# Welcome to ElysiaJS

It's great to have you here! This playground is designed to help you get started with ElysiaJS quickly and easily.

Unlike traditional backend framework, Elysia can also run in a browser! Allowing you to write, and try out Elysia directly in your browser! making it a perfect environment for learning and experimentation.

Elysia is an ergonomic web framework for humans.

---

---
url: 'https://elysiajs.com/tutorial/getting-started/plugin.md'
---

# Plugin

Every Elysia instance can be plug-and-play with other instances using the `use` method.

```typescript
import { Elysia } from 'elysia'

const user = new Elysia()
	.get('/profile', 'User Profile')
	.get('/settings', 'User Settings')

new Elysia()
	.use(user) // [!code ++]
	.get('/', 'Home')
	.listen(3000)
```

Once applied, all routes from `user` instance will be available in `app` instance.

### Plugin Config

You can also create a plugin that takes an argument and returns an Elysia instance to make a more dynamic plugin.

```typescript
import { Elysia } from 'elysia'

const user = ({ log = false }) => new Elysia() // [!code ++]
	.onBeforeHandle(({ request }) => {
		if (log) console.log(request)
	})
	.get('/profile', 'User Profile')
	.get('/settings', 'User Settings')

new Elysia()
	.use(user({ log: true })) // [!code ++]
	.get('/', 'Home')
	.listen(3000)
```

It's also recommended that you read about [Key Concept: Dependency](/key-concept#dependency) to understand how Elysia handles dependencies between plugins.

## Assignment

Let's apply the `user` instance to the `app` instance.

\<template #answer>

Similar to the above example, we can use the `use` method to plug the `user` instance into the `app` instance.

```typescript
import { Elysia } from 'elysia'

const user = new Elysia()
	.get('/profile', 'User Profile')
	.get('/settings', 'User Settings')

const app = new Elysia()
	.use(user) // [!code ++]
	.get('/', 'Home')
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/essential/plugin.md'
---

# Plugin&#x20;

A plugin is a part that is **decoupled** from the main instance.

Every Elysia instance can run independently or be used as part of another instance.

```typescript twoslash
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .decorate('plugin', 'hi')
    .get('/plugin', ({ plugin }) => plugin)

const app = new Elysia()
    .use(plugin)
    .get('/', ({ plugin }) => plugin)
               // ^?
    .listen(3000)
```

We can use the plugin by passing an instance to **Elysia.use**.

The plugin will inherit all properties of the plugin instance like `state`, `decorate` but **WILL NOT inherit plugin [lifecycle](/essential/life-cycle)** as it's [isolated by default](#scope) (mentioned in the next section ↓).

Elysia will also handle the type inference automatically as well.

::: tip
It's highly recommended that you have read [Key Concept: Dependency](/key-concept.html#dependency) before continuing.
:::

## Dependency&#x20;

Elysia, by design, is composed of multiple mini Elysia apps which can run **independently** like microservices that communicate with each other.

Each Elysia instance is independent and **can run as a standalone server**.

When an instance needs to use another instance's service, you **must explicitly declare the dependency**.

```ts twoslash
// @errors: 2339
import { t } from 'elysia'

abstract class Auth {
	static getProfile() {
		return {
			name: 'Elysia User'
		}
	}

	static models = {
		user: t.Object({
			name: t.String()
		})
	} as const
}
// ---cut---
import { Elysia } from 'elysia'

const auth = new Elysia()
	.decorate('Auth', Auth)
	.model(Auth.models)

const main = new Elysia()
 	// ❌ 'auth' is missing
	.get('/', ({ Auth }) => Auth.getProfile())
	// auth is required to use Auth's service
	.use(auth) // [!code ++]
	.get('/profile', ({ Auth }) => Auth.getProfile())
//                                        ^?



// ---cut-after---
```

This is similar to **Dependency Injection** where each instance must declare its dependencies.

This approach force you to be explicit about dependencies allowing better tracking, modularity.

### Deduplication&#x20;

By default, each plugin will be re-executed **every time** applying to another instance.

To prevent this, Elysia can deduplicate [lifecycle](/essential/life-cycle) with **a unique identifier** using `name` and optional `seed` property.

```ts
import { Elysia } from 'elysia'

// `name` is an unique identifier
const ip = new Elysia({ name: 'ip' }) // [!code ++]
	.derive(
		{ as: 'global' },
		({ server, request }) => ({
			ip: server?.requestIP(request)
		})
	)
	.get('/ip', ({ ip }) => ip)

const router1 = new Elysia()
	.use(ip)
	.get('/ip-1', ({ ip }) => ip)

const router2 = new Elysia()
	.use(ip)
	.get('/ip-2', ({ ip }) => ip)

const server = new Elysia()
	.use(router1)
	.use(router2)
```

Adding the `name` and optional `seed` to the instance will make it a unique identifier to prevent it from being called multiple times.

Learn more about this in [plugin deduplication](/essential/plugin.html#plugin-deduplication).

### Global vs Explicit Dependency

There are some cases where global dependency makes more sense than an explicit one.

**Global** plugin example:

* **Plugin that doesn't add types** - eg. cors, compress, helmet
* Plugin that add global [lifecycle](/essential/life-cycle) that no instance should have control over - eg. tracing, logging

Example use cases:

* OpenAPI/Open - Global document
* OpenTelemetry - Global tracer
* Logging - Global logger

In cases like this, it makes more sense to create it as a global dependency instead of applying it to every instance.

However, if your dependency doesn't fit into these categories, it's recommended to use **explicit dependency** instead.

**Explicit dependency** example:

* **Plugin that add types** - eg. macro, state, model
* Plugin that add business logic that instance can interact with - eg. Auth, Database

Example use cases:

* State management - eg. Store, Session
* Data modeling - eg. ORM, ODM
* Business logic - eg. Auth, Database
* Feature module - eg. Chat, Notification

## Scope &#x20;

Elysia [lifecycle](/essential/life-cycle) methods are **encapsulated** within their own instance.

This means if you create a new instance, it will not share the lifecycle methods with other instances.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(({ cookie }) => {
		throwIfNotSignIn(cookie)
	})
	.get('/profile', () => 'Hi there!')

const app = new Elysia()
	.use(profile)
	// ⚠️ This will NOT have a sign-in check
	.patch('/rename', ({ body }) => updateProfile(body))
```

In this example, the `isSignIn` check will only apply to `profile` but not `app`.

> Try changing the path in the URL bar to **/rename** and see the result

**Elysia isolate [lifecycle](/essential/life-cycle) by default** unless explicitly stated. This is similar to **export** in JavaScript, where you need to export the function to make it available outside the module.

To **"export"** the lifecycle to other instances, you must specify the scope.

```ts
import { Elysia } from 'elysia'

const profile = new Elysia()
	.onBeforeHandle(
		{ as: 'global' }, // [!code ++]
		({ cookie }) => {
			throwIfNotSignIn(cookie)
		}
	)
	.get('/profile', () => 'Hi there!')

const app = new Elysia()
	.use(profile)
	// This has sign in check
	.patch('/rename', ({ body }) => updateProfile(body))
```

Casting lifecycle to **"global"** will export lifecycle to **every instance**.

### Scope level

Elysia has 3 levels of scope as the following:

Scope types are as follows:

1. **local** (default) - applies to the current instance and its descendants only
2. **scoped** - applies to the parent, current instance, and descendants
3. **global** - applies to all instances that use the plugin (all parents, current, and descendants)

Let's review what each scope level does by using the following example:

```typescript
import { Elysia } from 'elysia'


const child = new Elysia()
    .get('/child', 'hi')

const current = new Elysia()
	// ? Value based on the table provided below
    .onBeforeHandle({ as: 'local' }, () => { // [!code ++]
        console.log('hi')
    })
    .use(child)
    .get('/current', 'hi')

const parent = new Elysia()
    .use(current)
    .get('/parent', 'hi')

const main = new Elysia()
    .use(parent)
    .get('/main', 'hi')
```

By changing the `type` value, the result should be as follows:

| type       | child | current | parent | main |
| ---------- | ----- | ------- | ------ | ---- |
| local      | ✅    | ✅      | ❌      | ❌   |
| scoped     | ✅    | ✅      | ✅      | ❌   |
| global     | ✅    | ✅      | ✅      | ✅   |

### Descendant

By default, a plugin will **apply a hook to itself and its descendants** only.

If the hook is registered in a plugin, instances that use the plugin will **NOT** inherit hooks and schema.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .onBeforeHandle(() => {
        console.log('hi')
    })
    .get('/child', 'log hi')

const main = new Elysia()
    .use(plugin)
    .get('/parent', 'not log hi')
```

To apply a hook globally, we need to specify the hook as global.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .onBeforeHandle(() => {
        return 'hi'
    })
    .get('/child', 'child')
    .as('scoped')

const main = new Elysia()
    .use(plugin)
    .get('/parent', 'parent')
```

## Config

To make the plugin more useful, allowing customization via config is recommended.

You can create a function that accepts parameters that may change the behavior of the plugin to make it more reusable.

```typescript
import { Elysia } from 'elysia'

const version = (version = 1) => new Elysia()
        .get('/version', version)

const app = new Elysia()
    .use(version(1))
    .listen(3000)
```

### Functional callback

It's recommended to define a new plugin instance instead of using a function callback.

Functional callbacks allow access to existing properties of the main instance. For example, checking if specific routes or stores exist, but they make encapsulation and scope harder to handle correctly.

To define a functional callback, create a function that accepts Elysia as a parameter.

```typescript
import { Elysia } from 'elysia'

const plugin = (app: Elysia) => app
    .state('counter', 0)
    .get('/plugin', () => 'Hi')

const app = new Elysia()
    .use(plugin)
    .get('/counter', ({ store: { counter } }) => counter)
    .listen(3000)
```

Once passed to `Elysia.use`, functional callback behaves as a normal plugin except the property is assigned directly to the main instance.

::: tip
You should not worry about the performance difference between a functional callback and creating an instance.

Elysia can create 10k instances in a matter of milliseconds, the new Elysia instance has even better type inference performance than the functional callback.
:::

## Guard&#x20;

Guard allows you to apply a hook and schema to multiple routes all at once.

```typescript twoslash
const signUp = <T>(a: T) => a
const signIn = <T>(a: T) => a
const isUserExists = <T>(a: T) => a
// ---cut---
import { Elysia, t } from 'elysia'

new Elysia()
    .guard(
        { // [!code ++]
            body: t.Object({ // [!code ++]
                username: t.String(), // [!code ++]
                password: t.String() // [!code ++]
            }) // [!code ++]
        }, // [!code ++]
        (app) => // [!code ++]
            app
                .post('/sign-up', ({ body }) => signUp(body))
                .post('/sign-in', ({ body }) => signIn(body), {
                                                     // ^?
                    beforeHandle: isUserExists
                })
    )
    .get('/', 'hi')
    .listen(3000)
```

This code applies validation for `body` to both '/sign-in' and '/sign-up' instead of inlining the schema one by one, but does not apply to '/'.

We can summarize the route validation as the following:
| Path | Has validation |
| ------- | ------------- |
| /sign-up | ✅ |
| /sign-in | ✅ |
| / | ❌ |

Guard accepts the same parameters as inline hooks; the only difference is that you can apply a hook to multiple routes in the scope.

This means that the code above is translated into:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .post('/sign-up', ({ body }) => signUp(body), {
        body: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
    .post('/sign-in', ({ body }) => body, {
        beforeHandle: isUserExists,
        body: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
    .get('/', () => 'hi')
    .listen(3000)
```

### Grouped Guard

We can use a group with prefixes by providing 3 parameters to the group.

1. Prefix - Route prefix
2. Guard - Schema
3. Scope - Elysia app callback

With the same API as guard apply to the 2nd parameter, instead of nesting group and guard together.

Consider the following example:

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
    .group('/v1', (app) =>
        app.guard(
            {
                body: t.Literal('Rikuhachima Aru')
            },
            (app) => app.post('/student', ({ body }) => body)
                                            // ^?
        )
    )
    .listen(3000)
```

From nested grouped guards, we can merge group and guard together by providing guard scope to the 2nd parameter of group:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .group(
        '/v1',
        (app) => app.guard( // [!code --]
        {
            body: t.Literal('Rikuhachima Aru')
        },
        (app) => app.post('/student', ({ body }) => body)
        ) // [!code --]
    )
    .listen(3000)
```

This results in the following syntax:

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
    .group(
        '/v1',
        {
            body: t.Literal('Rikuhachima Aru')
        },
        (app) => app.post('/student', ({ body }) => body)
                                       // ^?
    )
    .listen(3000)
```

## Scope cast Advanced Concept

To apply a hook to a parent, you may use one of the following:

1. [inline as](#inline-as) applies to only a single hook
2. [guard as](#guard-as) applies to all hooks in a guard
3. [instance as](#instance-as) applies to all hooks in an instance

### Inline as

Every event listener will accept `as` parameter to specify the scope of the hook.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .derive({ as: 'scoped' }, () => { // [!code ++]
        return { hi: 'ok' }
    })
    .get('/child', ({ hi }) => hi)

const main = new Elysia()
    .use(plugin)
    // ✅ Hi is now available
    .get('/parent', ({ hi }) => hi)
```

However, this method applies to only a single hook and may not be suitable for multiple hooks.

### Guard as

Every event listener will accept `as` parameter to specify the scope of the hook.

```typescript
import { Elysia, t } from 'elysia'

const plugin = new Elysia()
	.guard({
		as: 'scoped', // [!code ++]
		response: t.String(),
		beforeHandle() {
			console.log('ok')
		}
	})
    .get('/child', 'ok')

const main = new Elysia()
    .use(plugin)
    .get('/parent', 'hello')
```

Guard allows us to apply `schema` and `hook` to multiple routes all at once while specifying the scope.

However, it doesn't support `derive` and `resolve` method.

### Instance as

`as` reads all hooks and schema scopes of the current instance, modifying them.

```typescript
import { Elysia } from 'elysia'

const plugin = new Elysia()
    .derive(() => {
        return { hi: 'ok' }
    })
    .get('/child', ({ hi }) => hi)
    .as('scoped') // [!code ++]

const main = new Elysia()
    .use(plugin)
    // ✅ Hi is now available
    .get('/parent', ({ hi }) => hi)
```

Sometimes we want to reapply plugin to parent instance as well but as it's limited by `scoped` mechanism, it's limited to 1 parent only.

To apply to the parent instance, we need to **lift the scope up** to the parent instance, and `as` is the perfect method to do so.

Which means if you have `local` scope, and want to apply it to the parent instance, you can use `as('scoped')` to lift it up.

```typescript twoslash
// @errors: 2304 2345
import { Elysia, t } from 'elysia'

const plugin = new Elysia()
	.guard({
		response: t.String()
	})
	.onBeforeHandle(() => { console.log('called') })
	.get('/ok', () => 'ok')
	.get('/not-ok', () => 1)
	.as('scoped') // [!code ++]

const instance = new Elysia()
	.use(plugin)
	.get('/no-ok-parent', () => 2)
	.as('scoped') // [!code ++]

const parent = new Elysia()
	.use(instance)
	// This now error because `scoped` is lifted up to parent
	.get('/ok', () => 3)
```

## Lazy Load

Modules are eagerly loaded by default.

Elysia will make sure that all modules are registered before the server starts.

However, some modules may be computationally heavy or blocking, making the server startup slow.

To solve this, Elysia allows you to provide an async plugin that will not block the server startup.

### Deferred Module

The deferred module is an async plugin that can be registered after the server is started.

```typescript
// plugin.ts
import { Elysia, file } from 'elysia'
import { loadAllFiles } from './files'

export const loadStatic = async (app: Elysia) => {
    const files = await loadAllFiles()

    files.forEach((asset) => app
        .get(asset, file(file))
    )

    return app
}
```

And in the main file:

```typescript
import { Elysia } from 'elysia'
import { loadStatic } from './plugin'

const app = new Elysia()
    .use(loadStatic)
```

### Lazy Load Module

Same as an async plugin, the lazy-load module will be registered after the server is started.

A lazy-load module can be either synchronous or asynchronous; as long as the module is used with `import`, the module will be lazy-loaded.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
    .use(import('./plugin'))
```

Using module lazy-loading is recommended when the module is computationally heavy and/or blocking.

To ensure module registration before the server starts, we can use `await` on the deferred module.

### Testing

In a test environment, we can use `await app.modules` to wait for deferred and lazy-loading modules.

```typescript
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'

describe('Modules', () => {
    it('inline async', async () => {
        const app = new Elysia()
              .use(async (app) =>
                  app.get('/async', () => 'async')
              )

        await app.modules

        const res = await app
            .handle(new Request('http://localhost/async'))
            .then((r) => r.text())

        expect(res).toBe('async')
    })
})
```

---

---
url: 'https://elysiajs.com/plugins/overview.md'
---

# Overview

Elysia is designed to be modular and lightweight.

Following the same idea as Arch Linux (btw, I use Arch):

> Design decisions are made on a case-by-case basis through developer consensus

This is to ensure developers end up with a performant web server they intend to create. By extension, Elysia includes pre-built common pattern plugins for convenient developer usage:

## Official plugins

Here are some of the official plugins maintained by the Elysia team:

* [Bearer](/plugins/bearer) - retrieve [Bearer](https://swagger.io/docs/specification/authentication/bearer-authentication/) token automatically
* [CORS](/plugins/cors) - set up [Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
* [Cron](/plugins/cron) - set up [cron](https://en.wikipedia.org/wiki/Cron) job
* [Eden](/eden/overview) - end-to-end type safety client for Elysia
* [GraphQL Apollo](/plugins/graphql-apollo) - run [Apollo GraphQL](https://www.apollographql.com/) on Elysia
* [GraphQL Yoga](/plugins/graphql-yoga) - run [GraphQL Yoga](https://github.com/dotansimha/graphql-yoga) on Elysia
* [HTML](/plugins/html) - handle HTML responses
* [JWT](/plugins/jwt) - authenticate with [JWTs](https://jwt.io/)
* [OpenAPI](/plugins/openapi) - generate an [OpenAPI](https://swagger.io/specification/) documentation
* [OpenTelemetry](/plugins/opentelemetry) - add support for OpenTelemetry
* [Server Timing](/plugins/server-timing) - audit performance bottlenecks with the [Server-Timing API](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing)
* [Static](/plugins/static) - serve static files/folders

## Community plugins

* [Create ElysiaJS](https://github.com/kravetsone/create-elysiajs) - scaffold your Elysia project with the environment easily (help with ORM, Linters and Plugins)!
* [Lucia Auth](https://github.com/pilcrowOnPaper/lucia) - authentication that is simple and clean
* [Elysia Clerk](https://github.com/wobsoriano/elysia-clerk) - unofficial Clerk authentication plugin
* [Elysia Polyfills](https://github.com/bogeychan/elysia-polyfills) - run Elysia ecosystem on Node.js and Deno
* [Vite server](https://github.com/kravetsone/elysia-vite-server) - plugin which starts and decorates the [`vite`](https://vitejs.dev/) dev server in `development` and in `production` modes and serves static files (if needed)
* [Vite](https://github.com/timnghg/elysia-vite) - serve entry HTML file with Vite's scripts injected
* [Nuxt](https://github.com/trylovetom/elysiajs-nuxt) - easily integrate Elysia with Nuxt!
* [Remix](https://github.com/kravetsone/elysia-remix) - use [Remix](https://remix.run/) with `HMR` support (powered by [`vite`](https://vitejs.dev/))! Closes a really long-standing plugin request [#12](https://github.com/elysiajs/elysia/issues/12)
* [Sync](https://github.com/johnny-woodtke/elysiajs-sync) - a lightweight offline-first data synchronization framework powered by [Dexie.js](https://dexie.org/)
* [Connect middleware](https://github.com/kravetsone/elysia-connect-middleware) - plugin which allows you to use [`express`](https://www.npmjs.com/package/express)/[`connect`](https://www.npmjs.com/package/connect) middleware directly in Elysia!
* [Elysia HTTP Exception](https://github.com/codev911/elysia-http-exception) - Elysia plugin for HTTP 4xx/5xx error handling with structured exception classes
* [Elysia Helmet](https://github.com/DevTobias/elysia-helmet) - secure Elysia apps with various HTTP headers
* [Vite Plugin SSR](https://github.com/timnghg/elysia-vite-plugin-ssr) - Vite SSR plugin using Elysia server
* [OAuth 2.0](https://github.com/kravetsone/elysia-oauth2) - a plugin for [OAuth 2.0](https://en.wikipedia.org/wiki/OAuth) Authorization Flow with more than **42** providers and **type-safety**!
* [OAuth2](https://github.com/bogeychan/elysia-oauth2) - handle OAuth 2.0 authorization code flow
* [OAuth2 Resource Server](https://github.com/ap-1/elysia-oauth2-resource-server) - a plugin for validating JWT tokens from OAuth2 providers against JWKS endpoints with support for issuer, audience, and scope verification
* [Elysia OpenID Client](https://github.com/macropygia/elysia-openid-client) - OpenID client based on [openid-client](https://github.com/panva/node-openid-client)
* [Rate Limit](https://github.com/rayriffy/elysia-rate-limit) - simple, lightweight rate limiter
* [Elysia Nazli](https://github.com/esbuker/elysia-nazli) - Ergonomic, store-pluggable rate limiter with global and per-route rules.
* [LLMs.txt](https://github.com/opuu/elysia-llms-txt) - generate `/llms.txt` for LLM-friendly docs from OpenAPI/Swagger
* [Logysia](https://github.com/tristanisham/logysia) - classic logging middleware
* [Logestic](https://github.com/cybercoder-naj/logestic) - an advanced and customizable logging library for ElysiaJS
* [Logger](https://github.com/bogeychan/elysia-logger) - [pino](https://github.com/pinojs/pino)-based logging middleware
* [Elysia Line](https://github.com/KrataiB/elysia-line) - LINE Messaging API and LINE Login integration for Elysia (wrapper around the official [@line/bot-sdk](https://github.com/line/line-bot-sdk-nodejs))
* [Elylog](https://github.com/eajr/elylog) - simple stdout logging library with some customization
* [Logify for Elysia.js](https://github.com/0xrasla/logify) - a beautiful, fast, and type-safe logging middleware for Elysia.js applications
* [Nice Logger](https://github.com/tanishqmanuja/nice-logger) - not the nicest, but a pretty nice and sweet logger for Elysia
* [LogTape for Elysia](https://logtape.org/manual/integrations#elysia) - structured logging middleware with support for multiple sinks (transports) through [LogTape](https://logtape.org/)
* [Sentry](https://github.com/johnny-woodtke/elysiajs-sentry) - capture traces and errors with this [Sentry](https://docs.sentry.io/) plugin
* [Apitally](https://github.com/apitally/apitally-js) - capture metrics, logs, and traces in [Apitally](https://apitally.io/elysia), a simple API monitoring and analytics tool
* [Elysia Lambda](https://github.com/TotalTechGeek/elysia-lambda) - deploy on AWS Lambda
* [Decorators](https://github.com/gaurishhs/elysia-decorators) - use TypeScript decorators
* [Elysia FSR](https://github.com/deadlinecode/elysia-fsr) - file-system routing with Eden-compatible type generation, monorepo/workspace support, and logical route grouping
* [Autoload](https://github.com/kravetsone/elysia-autoload) - filesystem router based on a directory structure that generates types for [Eden](/eden/overview) with [`Bun.build`](https://github.com/kravetsone/elysia-autoload?tab=readme-ov-file#bun-build-usage) support
* [Msgpack](https://github.com/kravetsone/elysia-msgpack) - allows you to work with [MessagePack](https://msgpack.org)
* [XML](https://github.com/kravetsone/elysia-xml) - allows you to work with XML
* [Autoroutes](https://github.com/wobsoriano/elysia-autoroutes) - filesystem routes
* [Group Router](https://github.com/itsyoboieltr/elysia-group-router) - filesystem and folder-based router for groups
* [Basic Auth](https://github.com/itsyoboieltr/elysia-basic-auth) - basic HTTP authentication
* [Body Limit](https://github.com/hexadecimal233/elysia-body-limit) - limit body sizes in Elysia
* [ETag](https://github.com/bogeychan/elysia-etag) - automatic HTTP [ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag) generation
* [CDN Cache](https://github.com/johnny-woodtke/elysiajs-cdn-cache) - Cache-Control plugin for Elysia - no more manually setting HTTP headers
* [Basic Auth](https://github.com/eelkevdbos/elysia-basic-auth) - basic HTTP authentication (using `request` event)
* [i18n](https://github.com/eelkevdbos/elysia-i18next) - [i18n](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/i18n) wrapper based on [i18next](https://www.i18next.com/)
* [Intlify](https://github.com/intlify/srvmid/blob/main/packages/elysia/README.md) - Internationalization server middleware & utilities
* [Elysia Request ID](https://github.com/gtramontina/elysia-requestid) - add/forward request IDs (`X-Request-ID` or custom)
* [Elysia HTMX](https://github.com/gtramontina/elysia-htmx) - context helpers for [HTMX](https://htmx.org/)
* [Elysia HMR HTML](https://github.com/gtrabanco/elysia-hmr-html) - reload HTML files when changing any file in a directory
* [Elysia Inject HTML](https://github.com/gtrabanco/elysia-inject-html) - inject HTML code in HTML files
* [Elysia HTTP Error](https://github.com/yfrans/elysia-http-error) - return HTTP errors from Elysia handlers
* [Elysia Http Status Code](https://github.com/sylvain12/elysia-http-status-code) - integrate HTTP status codes
* [NoCache](https://github.com/gaurishhs/elysia-nocache) - disable caching
* [Elysia Tailwind](https://github.com/gtramontina/elysia-tailwind) - compile [Tailwindcss](https://tailwindcss.com/) in a plugin.
* [tailwind-serve](https://github.com/Moshyfawn/tailwind-serve) - compile and serve [Tailwind CSS v4](https://tailwindcss.com/) at runtime with no build step, works with any server framework
* [Elysia Compression](https://github.com/gusb3ll/elysia-compression) - compress response
* [Elysia IP](https://github.com/gaurishhs/elysia-ip) - get the IP Address
* [OAuth2 Server](https://github.com/myazarc/elysia-oauth2-server) - develop an OAuth2 server with Elysia
* [Elysia Flash Messages](https://github.com/gtramontina/elysia-flash-messages) - enable flash messages
* [Elysia AuthKit](https://github.com/gtramontina/elysia-authkit) - unofficial [WorkOS' AuthKit](https://www.authkit.com/) authentication
* [Elysia Error Handler](https://github.com/gtramontina/elysia-error-handler) - simpler error handling
* [Elysia env](https://github.com/yolk-oss/elysia-env) - typesafe environment variables with typebox
* [Elysia Drizzle Schema](https://github.com/Edsol/elysia-drizzle-schema) - helps use Drizzle ORM schema inside Elysia OpenAPI model
* [Unify-Elysia](https://github.com/qlaffont/unify-elysia) - unify error codes for Elysia
* [Unify-Elysia-GQL](https://github.com/qlaffont/unify-elysia-gql) - unify error codes for Elysia GraphQL Server (Yoga & Apollo)
* [Elysia Auth Drizzle](https://github.com/qlaffont/elysia-auth-drizzle) - library that handles authentication with JWT (Header/Cookie/QueryParam)
* [graceful-server-elysia](https://github.com/qlaffont/graceful-server-elysia) - library inspired by [graceful-server](https://github.com/gquittet/graceful-server)
* [Logixlysia](https://github.com/PunGrumpy/logixlysia) - a beautiful and simple logging middleware for ElysiaJS with colors and timestamps.
* [Elysia Fault](https://github.com/vitorpldev/elysia-fault) - a simple and customizable error handling middleware with the possibility of creating your own HTTP errors
* [Elysia Compress](https://github.com/vermaysha/elysia-compress) - ElysiaJS plugin to compress responses inspired by [@fastify/compress](https://github.com/fastify/fastify-compress)
* [@labzzhq/compressor](https://github.com/labzzhq/compressor/) - Compact Brilliance, Expansive Results: HTTP Compressor for Elysia and Bunnyhop with gzip, deflate and brotli support.
* [Elysia Accepts](https://github.com/morigs/elysia-accepts) - Elysia plugin for accept headers parsing and content negotiation
* [Elysia Compression](https://github.com/chneau/elysia-compression) - Elysia plugin for compressing responses
* [Elysia Logger](https://github.com/chneau/elysia-logger) - Elysia plugin for logging HTTP requests and responses inspired by [hono/logger](https://hono.dev/docs/middleware/builtin/logger)
* [Elysia CQRS](https://github.com/jassix/elysia-cqrs) - Elysia plugin for CQRS pattern
* [Elysia Supabase](https://github.com/mastermakrela/elysia-supabase) - Seamlessly integrate [Supabase](https://supabase.com/) authentication and database functionality into Elysia, allowing easy access to authenticated user data and Supabase client instance. Especially useful for [Edge Functions](https://supabase.com/docs/guides/functions).
* [Elysia XSS](https://www.npmjs.com/package/elysia-xss) - a plugin for Elysia.js that provides XSS (Cross-Site Scripting) protection by sanitizing request body data.
* [Elysiajs Helmet](https://www.npmjs.com/package/elysiajs-helmet) - a comprehensive security middleware for Elysia.js applications that helps secure your apps by setting various HTTP headers.
* [Decorators for Elysia.js](https://github.com/Ateeb-Khan-97/better-elysia) - seamlessly develop and integrate APIs, WebSocket, and Streaming APIs with this small library.
* [Elysia Protobuf](https://github.com/ilyhalight/elysia-protobuf) - protobuf support for Elysia.
* [Elysia Prometheus](https://github.com/m1handr/elysia-prometheus) - Elysia plugin for exposing HTTP metrics for Prometheus.
* [Elysia Remote DTS](https://github.com/rayriffy/elysia-remote-dts) - A plugin that provides .d.ts types remotely for Eden Treaty to consume.
* [Cap Checkpoint plugin for Elysia](https://capjs.js.org/guide/middleware/elysia.html) - Cloudflare-like middleware for Cap, a lightweight, modern open-source CAPTCHA alternative designed using SHA-256 PoW.
* [Elysia Background](https://github.com/staciax/elysia-background) - A background task processing plugin for Elysia.js
* [Elysia External Session - TS only GitHub package](https://github.com/extend-therapy/elysia-external-session) - A sessions package for Redis and SQLite that is extensible and uses the current Elysia architecture.
* [@fedify/elysia](https://github.com/fedify-dev/fedify/tree/main/packages/elysia) - A plugin that provides seamless integration with [Fedify](https://fedify.dev/), the ActivityPub server framework.
* [elysia-healthcheck](https://github.com/iam-medvedev/elysia-healthcheck) - Healthcheck plugin for Elysia.js
* [elysia-csrf](https://github.com/lauhon/elysia-csrf) - A CSRF plugin, ported from [express-csrf](https://github.com/expressjs/csurf)
* [elysia-local-https](https://github.com/mrtcmn/elysia-local-https) - Automatic local HTTPS for Elysia — certs generated, managed, and refreshed in one line.
* [elysia-circuit-breaker](https://github.com/camargo-leonardo/elysia-circuit-breaker) - A Circuit Breaker plugin that brings fault tolerance to Elysia.js.
* [Eden TanStack Query](https://github.com/xkelxmc/eden-tanstack-query) - type-safe TanStack Query integration for Eden, like
  @trpc/react-query but for Elysia
* [Socket.IO Proxy](https://www.npmjs.com/package/@synchjs/elysocket) - Socket.IO Proxy for Elysia.
* [ModernCSRF](https://github.com/auto-medica-labs/modern-csrf) - A lightweight, token-free CSRF protection middleware for ElysiaJS
* [elysia-wide-event](https://github.com/choiexe1/elysia-wide-event) - Wide event logging plugin for structured request-level observability.
* [elysia-beta-headers](https://github.com/P0u4a/elysia-beta-headers) - Elysia plugin for gating your app's beta/experimental features via type-safe API headers
* [elysia-better-session](https://github.com/0x0arash/elysia-better-session) - Elysia plugin for server-side session management with different store adapters.

## Complementary projects:

* [prismabox](https://github.com/m1212e/prismabox) - Generator for TypeBox schemas based on your database models, works well with Elysia

## Project templates:

* [ElysiaTemplate](https://github.com/QLing-yes/ElysiaTemplate) - MVC backend, auto route & middleware, more coming.

***

If you have a plugin written for Elysia, feel free to add your plugin to the list by **clicking Edit this page on GitHub** below 👇

---

---
url: 'https://elysiajs.com/playground/preview.md'
---


---

---
url: 'https://elysiajs.com/quick-start.md'
---

# Quick Start

Elysia is a TypeScript backend framework with multiple runtime support but optimized for Bun.

However, you can use Elysia with other runtimes like Node.js.

\<Tab
id="quickstart"
:names="\['Bun', 'Node.js', 'Web Standard']"
:tabs="\['bun', 'node', 'web-standard']"

>

Elysia is optimized for Bun which is a JavaScript runtime that aims to be a drop-in replacement for Node.js.

You can install Bun with the command below:

::: code-group

```bash [MacOS/Linux]
curl -fsSL https://bun.sh/install | bash
```

```bash [Windows]
powershell -c "irm bun.sh/install.ps1 | iex"
```

:::

\<Tab
id="quickstart"
:names="\['Auto Installation', 'Manual Installation']"
:tabs="\['auto', 'manual']"

>

We recommend starting a new Elysia server using `bun create elysia`, which sets up everything automatically.

```bash
bun create elysia app
```

Once done, you should see the folder name `app` in your directory.

```bash
cd app
```

Start a development server by:

```bash
bun dev
```

Navigate to [localhost:3000](http://localhost:3000), which should greet you with "Hello Elysia".

::: tip
Elysia provides a `dev` command to automatically reload your server on file changes.
:::

To manually create a new Elysia app, install Elysia as a package:

```typescript
bun add elysia
bun add -d @types/bun
```

This will install Elysia and Bun type definitions.

Create a new file `src/index.ts` and add the following code:

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', () => 'Hello Elysia')
	.listen(3000)

console.log(
	`🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

Open your `package.json` file and add the following scripts:

```json
{
   	"scripts": {
  		"dev": "bun --watch src/index.ts",
  		"build": "bun build src/index.ts --target bun --outdir ./dist",
  		"start": "NODE_ENV=production bun dist/index.js",
  		"test": "bun test"
   	}
}
```

These scripts refer to the different stages of developing an application:

* **dev** - Start Elysia in development mode with auto-reload on code change.
* **build** - Build the application for production usage.
* **start** - Start an Elysia production server.

If you are using TypeScript, make sure to create, and update `tsconfig.json` to include `compilerOptions.strict` to `true`:

```json
{
   	"compilerOptions": {
  		"strict": true
   	}
}
```

Node.js is a JavaScript runtime for server-side applications, the most popular runtime for JavaScript which Elysia supports.

You can install Node.js with the command below:

::: code-group

```bash [MacOS]
brew install node
```

```bash [Windows]
choco install nodejs
```

```bash [apt (Linux)]
sudo apt install nodejs
```

```bash [pacman (Arch)]
pacman -S nodejs npm
```

:::

## Setup

We recommend using TypeScript for your Node.js project.

\<Tab
id="language"
:names="\['TypeScript', 'JavaScript']"
:tabs="\['ts', 'js']"

>

To create a new Elysia app with TypeScript, we recommend installing Elysia with `tsx`:

::: code-group

```bash [bun]
bun add elysia @elysia/node && \
bun add -d tsx @types/node typescript
```

```bash [pnpm]
# pnpm doesn't install peer dependencies
pnpm add elysia @elysia/node @sinclair/typebox openapi-types && \
pnpm add -D tsx @types/node typescript
```

```bash [npm]
npm install elysia @elysia/node && \
npm install --save-dev tsx @types/node typescript
```

```bash [yarn]
yarn add elysia @elysia/node && \
yarn add -D tsx @types/node typescript
```

:::

This will install Elysia, TypeScript, and `tsx`.

`tsx` is a CLI that transpiles TypeScript to JavaScript with hot-reload and several more features you'd expect from a modern development environment.

Create a new file `src/index.ts` and add the following code:

```typescript
import { Elysia } from 'elysia'
import { node } from '@elysia/node'

const app = new Elysia({ adapter: node() })
	.get('/', () => 'Hello Elysia')
	.listen(3000, ({ hostname, port }) => {
		console.log(
			`🦊 Elysia is running at ${hostname}:${port}`
		)
	})
```

Open your `package.json` file and add the following scripts:

```json
{
   	"scripts": {
  		"dev": "tsx watch src/index.ts",
    	"build": "tsc src/index.ts --outDir dist",
  		"start": "NODE_ENV=production node dist/index.js"
   	}
}
```

These scripts refer to the different stages of developing an application:

* **dev** - Start Elysia in development mode with auto-reload on code change.
* **build** - Build the application for production usage.
* **start** - Start an Elysia production server.

Make sure to create `tsconfig.json`

```bash
npx tsc --init
```

Don't forget to update `tsconfig.json` to include `compilerOptions.strict` to `true`:

```json
{
   	"compilerOptions": {
  		"strict": true
   	}
}
```

::: warning
If you use Elysia without TypeScript, you may miss out on some features like auto-completion, advanced type checking, and end-to-end type safety, which are core features of Elysia.
:::

To create a new Elysia app with JavaScript, start by installing Elysia:

::: code-group

```bash [bun]
bun add elysia @elysia/node
```

```bash [pnpm]
# pnpm doesn't install peer dependencies
pnpm add elysia @elysia/node @sinclair/typebox openapi-types
```

```bash [npm]
npm install elysia @elysia/node
```

```bash [yarn]
yarn add elysia @elysia/node
```

:::

This will install Elysia.

Create a new file `src/index.js` and add the following code:

```javascript
import { Elysia } from 'elysia'
import { node } from '@elysia/node'

const app = new Elysia({ adapter: node() })
	.get('/', () => 'Hello Elysia')
	.listen(3000, ({ hostname, port }) => {
		console.log(
			`🦊 Elysia is running at ${hostname}:${port}`
		)
	})
```

Open your `package.json` file and add the following scripts:

```json
{
	"type": "module",
   	"scripts": {
  		"dev": "node src/index.js",
  		"start": "NODE_ENV=production node src/index.js"
   	}
}
```

These scripts refer to the different stages of developing an application:

* **dev** - Start Elysia in development mode.
* **start** - Start an Elysia production server.

::: warning
If you use Elysia without TypeScript, you may miss out on some features like auto-completion, advanced type checking, and end-to-end type safety, which are core features of Elysia.
:::

Elysia is a WinterTC compliant library, which means if a framework or runtime supports Web Standard Request/Response, it can run Elysia.

First, install Elysia with the command below:

::: code-group

```bash [bun]
bun install elysia
```

```bash [pnpm]
# pnpm doesn't install peer dependencies
pnpm install elysia @sinclair/typebox openapi-types
```

```bash [npm]
npm install elysia
```

```bash [yarn]
yarn add elysia
```

:::

Next, select a runtime that supports Web Standard Request/Response.

We have a few recommendations:

### Not on the list?

If you are using a custom runtime, you may access `app.fetch` to handle the request and response manually.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', () => 'Hello Elysia')
	.listen(3000)

export default app.fetch

console.log(
	`🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
)
```

---

---
url: 'https://elysiajs.com/integrations/react-email.md'
---

# React Email

React Email is a library that allows you to use React components to create emails.

As Elysia uses Bun as the runtime environment, we can directly write a React Email component and import the JSX directly into our code to send emails.

## Installation

To install React Email, run the following command:

```bash
bun add -d react-email
bun add @react-email/components react react-dom
```

Then add this script to `package.json`:

```json
{
  "scripts": {
    "email": "email dev --dir src/emails"
  }
}
```

We recommend adding email templates into the `src/emails` directory as we can directly import the JSX files.

### TypeScript

If you are using TypeScript, you may need to add the following to your `tsconfig.json`:

```json
{
  "compilerOptions": {
	"jsx": "react"
  }
}
```

## Your first email

Create file `src/emails/otp.tsx` with the following code:

```tsx
import * as React from 'react'
import { Tailwind, Section, Text } from '@react-email/components'

export default function OTPEmail({ otp }: { otp: number }) {
    return (
        <Tailwind>
            <Section className="flex justify-center items-center w-full min-h-screen font-sans">
                <Section className="flex flex-col items-center w-76 rounded-2xl px-6 py-1 bg-mauve-50">
                    <Text className="text-xs font-medium text-violet-500">
                        Verify your Email Address
                    </Text>
                    <Text className="text-mauve-500 my-0">
                        Use the following code to verify your email address
                    </Text>
                    <Text className="text-5xl font-bold pt-2">{otp}</Text>
                    <Text className="text-mauve-400 font-light text-xs pb-4">
                        This code is valid for 10 minutes
                    </Text>
                    <Text className="text-mauve-600 text-xs">
                        Thank you for joining us
                    </Text>
                </Section>
            </Section>
        </Tailwind>
    )
}

OTPEmail.PreviewProps = {
    otp: 123456
}
```

You may notice that we are using `@react-email/components` to create the email template.

This library provides a set of components including **styling with Tailwind** that are compatible with email clients like Gmail, Outlook, etc.

We also added a `PreviewProps` to the `OTPEmail` function. This only applies when previewing the email on our playground.

## Preview your email

To preview your email, run the following command:

```bash
bun email
```

This will open a browser window with the preview of your email.

![React Email playground showing an OTP email we have just written](/recipe/react-email/email-preview.webp)

## Sending email

To send an email, we can use `react-dom/server` to render the email, then submit it using a preferred provider:

::: code-group

```tsx [Nodemailer]
import { Elysia, t } from 'elysia'

import * as React from 'react'
import { renderToStaticMarkup } from 'react-dom/server'

import OTPEmail from './emails/otp'

import nodemailer from 'nodemailer' // [!code ++]

const transporter = nodemailer.createTransport({ // [!code ++]
  	host: 'smtp.gehenna.sh', // [!code ++]
  	port: 465, // [!code ++]
  	auth: { // [!code ++]
  		user: 'makoto', // [!code ++]
  		pass: '12345678' // [!code ++]
  	} // [!code ++]
}) // [!code ++]

new Elysia()
	.get('/otp', async ({ body }) => {
		// Random between 100,000 and 999,999
  		const otp = ~~(Math.random() * (900_000 - 1)) + 100_000

		const html = renderToStaticMarkup(<OTPEmail otp={otp} />)

        await transporter.sendMail({ // [!code ++]
        	from: 'ibuki@gehenna.sh', // [!code ++]
           	to: body, // [!code ++]
           	subject: 'Verify your email address', // [!code ++]
            html, // [!code ++]
        }) // [!code ++]

        return { success: true }
	}, {
		body: t.String({ format: 'email' })
	})
	.listen(3000)
```

```tsx [Resend]
import { Elysia, t } from 'elysia'

import OTPEmail from './emails/otp'

import Resend from 'resend' // [!code ++]

const resend = new Resend('re_123456789') // [!code ++]

new Elysia()
	.get('/otp', ({ body }) => {
		// Random between 100,000 and 999,999
  		const otp = ~~(Math.random() * (900_000 - 1)) + 100_000

        await resend.emails.send({ // [!code ++]
        	from: 'ibuki@gehenna.sh', // [!code ++]
           	to: body, // [!code ++]
           	subject: 'Verify your email address', // [!code ++]
            html: <OTPEmail otp={otp} />, // [!code ++]
        }) // [!code ++]

        return { success: true }
	}, {
		body: t.String({ format: 'email' })
	})
	.listen(3000)
```

```tsx [AWS SES]
import { Elysia, t } from 'elysia'

import * as React from 'react'
import { renderToStaticMarkup } from 'react-dom/server'

import OTPEmail from './emails/otp'

import { type SendEmailCommandInput, SES } from '@aws-sdk/client-ses' // [!code ++]
import { fromEnv } from '@aws-sdk/credential-providers' // [!code ++]

const ses = new SES({ // [!code ++]
    credentials: // [!code ++]
        process.env.NODE_ENV === 'production' ? fromEnv() : undefined // [!code ++]
}) // [!code ++]

new Elysia()
	.get('/otp', ({ body }) => {
		// Random between 100,000 and 999,999
  		const otp = ~~(Math.random() * (900_000 - 1)) + 100_000

		const html = renderToStaticMarkup(<OTPEmail otp={otp} />)

        await ses.sendEmail({ // [!code ++]
            Source: 'ibuki@gehenna.sh', // [!code ++]
            Destination: { // [!code ++]
                ToAddresses: [body] // [!code ++]
            }, // [!code ++]
            Message: { // [!code ++]
                Body: { // [!code ++]
                    Html: { // [!code ++]
                        Charset: 'UTF-8', // [!code ++]
                        Data: html // [!code ++]
                    } // [!code ++]
                }, // [!code ++]
                Subject: { // [!code ++]
                    Charset: 'UTF-8', // [!code ++]
                    Data: 'Verify your email address' // [!code ++]
                } // [!code ++]
            } // [!code ++]
        } satisfies SendEmailCommandInput) // [!code ++]

        return { success: true }
	}, {
		body: t.String({ format: 'email' })
	})
	.listen(3000)
```

```tsx [Sendgrid]
import { Elysia, t } from 'elysia'

import OTPEmail from './emails/otp'

import sendgrid from "@sendgrid/mail" // [!code ++]

sendgrid.setApiKey(process.env.SENDGRID_API_KEY) // [!code ++]

new Elysia()
	.get('/otp', ({ body }) => {
		// Random between 100,000 and 999,999
  		const otp = ~~(Math.random() * (900_000 - 1)) + 100_000

    	const html = renderToStaticMarkup(<OTPEmail otp={otp} />)

        await sendgrid.send({ // [!code ++]
        	from: 'ibuki@gehenna.sh', // [!code ++]
           	to: body, // [!code ++]
           	subject: 'Verify your email address', // [!code ++]
            html // [!code ++]
        }) // [!code ++]

        return { success: true }
	}, {
		body: t.String({ format: 'email' })
	})
	.listen(3000)
```

:::

::: tip
Notice that we can directly import the email component out of the box thanks to Bun
:::

You may see all of the available integrations with React Email in the [React Email Integrations](https://react.email/docs/integrations/overview), and learn more about React Email in the [React Email documentation](https://react.email/docs)

---

---
url: 'https://elysiajs.com/patterns/cookie.md'
---

# Cookie&#x20;

Elysia provides a mutable signal for interacting with Cookie.

There's no get/set, you can extract the cookie name and retrieve or update its value directly.

```ts
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { name } }) => {
        // Get
        name.value

        // Set
        name.value = "New Value"
    })
```

By default, Reactive Cookie can automatically encode/decode object types allowing us to treat cookies as objects without worrying about the encoding/decoding. **It just works**.

::: warning
You may get a warning when using cookie.name as it might be `undefined`

Elysia cookie can never be `undefined` because it's a Proxy object. `cookie` is always defined, only its value (via cookie.value) can be undefined.

This can be fixed by using \[a cookie schema] or disabling [strictNullChecks](https://www.typescriptlang.org/tsconfig/#strictNullChecks) in `tsconfig.json`
:::

## Reactivity

The Elysia cookie is reactive. This means that when you change the cookie value, the cookie will be updated automatically based on an approach like signals.

A single source of truth for handling cookies is provided by Elysia cookies, which have the ability to automatically set headers and sync cookie values.

Since cookies are Proxy-dependent objects by default, the extract value can never be **undefined**; instead, it will always be a value of `Cookie<unknown>`, which can be obtained by invoking the **.value** property.

We can treat the cookie jar as a regular object, iteration over it will only iterate over an already-existing cookie value.

## Cookie Attribute

To use Cookie attributes, you can use one of the following:

1. Setting the property directly
2. Using `set` or `add` to update cookie properties.

See [cookie attribute config](/patterns/cookie.html#config) for more information.

### Assign Property

You can get/set properties of a cookie like any normal object, the reactivity model synchronizes the cookie value automatically.

```ts
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { name } }) => {
        // get
        name.domain

        // set
        name.domain = 'millennium.sh'
        name.httpOnly = true
    })
```

## set

**set** permits updating multiple cookie properties all at once through **reset all property** and overwrite the property with a new value.

```ts
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { name } }) => {
        name.set({
            domain: 'millennium.sh',
            httpOnly: true
        })
    })
```

## add

Like **set**, **add** allows us to update multiple cookie properties at once, but instead will only overwrite the properties defined instead of resetting.

## remove

To remove a cookie, you can use either:

1. name.remove
2. delete cookie.name

```ts
import { Elysia } from 'elysia'

new Elysia()
    .get('/', ({ cookie, cookie: { name } }) => {
        name.remove()

        delete cookie.name
    })
```

## Cookie Schema

You can strictly validate cookie type and provide type inference for cookies by using cookie schema with `t.Cookie`.

```ts
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { name } }) => {
        // Set
        name.value = {
            id: 617,
            name: 'Summoning 101'
        }
    }, {
        cookie: t.Cookie({
            name: t.Object({
                id: t.Numeric(),
                name: t.String()
            })
        })
    })
```

## Nullable Cookie

To handle nullable cookie value, you can use `t.Optional` on the cookie name you want to be nullable.

```ts
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { name } }) => {
        // Set
        name.value = {
            id: 617,
            name: 'Summoning 101'
        }
    }, {
        cookie: t.Cookie({
            name: t.Optional(
                t.Object({
                    id: t.Numeric(),
                    name: t.String()
                })
            )
        })
    })
```

## Cookie Signature

With the introduction of Cookie Schema and `t.Cookie` type, we can create a unified type for handling sign/verify cookie signature automatically.

Cookie signature is a cryptographic hash appended to a cookie's value, generated using a secret key and the content of the cookie to enhance security by adding a signature to the cookie.

This makes sure that the cookie value is not modified by malicious actors, helping verify the authenticity and integrity of the cookie data.

## Using Cookie Signature

By providing a cookie secret and `sign` property to indicate which cookie should have signature verification.

```ts
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/', ({ cookie: { profile } }) => {
        profile.value = {
            id: 617,
            name: 'Summoning 101'
        }
    }, {
        cookie: t.Cookie({
            profile: t.Object({
                id: t.Numeric(),
                name: t.String()
            })
        }, {
            secrets: 'Fischl von Luftschloss Narfidort',
            sign: ['profile']
        })
    })
```

Elysia then sign and unsign cookie value automatically.

## Constructor

You can use Elysia constructor to set global cookie `secret` and `sign` values to apply to all routes globally instead of inlining to every route you need.

```ts
import { Elysia, t } from 'elysia'

new Elysia({
    cookie: {
        secrets: 'Fischl von Luftschloss Narfidort',
        sign: ['profile']
    }
})
    .get('/', ({ cookie: { profile } }) => {
        profile.value = {
            id: 617,
            name: 'Summoning 101'
        }
    }, {
        cookie: t.Cookie({
            profile: t.Object({
                id: t.Numeric(),
                name: t.String()
            })
        })
    })
```

## Cookie Rotation

Elysia handles cookie secret rotation automatically.

Cookie Rotation is a migration technique to sign a cookie with a newer secret, while also be able to verify the old signature of the cookie.

```ts
import { Elysia } from 'elysia'

new Elysia({
    cookie: {
        secrets: ['Vengeance will be mine', 'Fischl von Luftschloss Narfidort']
    }
})
```

### Unsigned Cookie Transition

Elysia supports graceful transition from unsigned to signed cookies.

By setting `null` in an array of `cookie.secrets`, Elysia will allow unsigned cookies to pass through while checking invalid cookie signatures when available.

```ts
import { Elysia } from 'elysia'

new Elysia({
    cookie: {
        secrets: ['Vengeance will be mine', 'Fischl von Luftschloss Narfidort', null]
    }
})
```

Elysia will then use the first `secrets` to sign the new cookie allowing graceful transition.

It's recommended to only allow unsigned cookies during the transition period to prevent unsafe cookies from occurring.

## Config

Below is a cookie config accepted by Elysia.

### secret

The secret key for signing/verifying cookies.

If an array is passed, it will use Key Rotation.

Key rotation is when an encryption key is retired and replaced by generating a new cryptographic key.

***

Below is a config that extends from [cookie](https://npmjs.com/package/cookie)

### domain

Specifies the value for the [Domain Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.3).

By default, no domain is set, and most clients will consider the cookie to apply to only the current domain.

### encode

@default `encodeURIComponent`

Specifies a function that will be used to encode a cookie value.

Since the value of a cookie has a limited character set (and must be a simple string), this function can be used to encode a value into a string suited for a cookie value.

The default function is the global `encodeURIComponent`, which will encode a JavaScript string into UTF-8 byte sequences and then URL-encode any that fall outside of the cookie range.

### expires

Specifies the Date object to be the value for the [Expires Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.1).

By default, no expiration is set, and most clients will consider this a "non-persistent cookie" and will delete it on conditions like exiting a web browser application.

::: tip
The [cookie storage model specification](https://tools.ietf.org/html/rfc6265#section-5.3) states that if both `expires` and `maxAge` are set, then `maxAge` takes precedence, but not all clients may obey this, so if both are set, they should point to the same date and time.
:::

### httpOnly

@default `false`

Specifies the boolean value for the [HttpOnly Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.6).

When truthy, the HttpOnly attribute is set, otherwise, it is not.

By default, the HttpOnly attribute is not set.

::: tip
be careful when setting this to true, as compliant clients will not allow client-side JavaScript to see the cookie in `document.cookie`.
:::

### maxAge

@default `undefined`

Specifies the number (in seconds) to be the value for the [Max-Age Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.2).

The given number will be converted to an integer by rounding down. By default, no maximum age is set.

::: tip
The [cookie storage model specification](https://tools.ietf.org/html/rfc6265#section-5.3) states that if both `expires` and `maxAge` are set, then `maxAge` takes precedence, but not all clients may obey this, so if both are set, they should point to the same date and time.
:::

### path

Specifies the value for the [Path Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.4).

By default, the path handler is considered the default path.

### priority

Specifies the string to be the value for the [Priority Set-Cookie attribute](https://tools.ietf.org/html/draft-west-cookie-priority-00#section-4.1).
`low` will set the Priority attribute to Low.
`medium` will set the Priority attribute to Medium, the default priority when not set.
`high` will set the Priority attribute to High.

More information about the different priority levels can be found in [the specification](https://tools.ietf.org/html/draft-west-cookie-priority-00#section-4.1).

::: tip
This is an attribute that has not yet been fully standardized and may change in the future. This also means many clients may ignore this attribute until they understand it.
:::

### sameSite

Specifies the boolean or string to be the value for the [SameSite Set-Cookie attribute](https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-09#section-5.4.7).
`true` will set the SameSite attribute to Strict for strict same-site enforcement.
`false` will not set the SameSite attribute.
`'lax'` will set the SameSite attribute to Lax for lax same-site enforcement.
`'none'` will set the SameSite attribute to None for an explicit cross-site cookie.
`'strict'` will set the SameSite attribute to Strict for strict same-site enforcement.
More information about the different enforcement levels can be found in [the specification](https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-09#section-5.4.7).

::: tip
This is an attribute that has not yet been fully standardized and may change in the future. This also means many clients may ignore this attribute until they understand it.
:::

### secure

Specifies the boolean value for the [Secure Set-Cookie attribute](https://tools.ietf.org/html/rfc6265#section-5.2.5). When truthy, the Secure attribute is set, otherwise, it is not. By default, the Secure attribute is not set.

::: tip
Be careful when setting this to true, as compliant clients will not send the cookie back to the server in the future if the browser does not have an HTTPS connection.
:::

---

---
url: 'https://elysiajs.com/essential/route.md'
---

# Routing&#x20;

Web servers use the request's **path and method** to look up the correct resource, known as **"routing"**.

We can define a route with **an HTTP verb method**, a path and a function to execute when matched.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', 'hello')
    .get('/hi', 'hi')
    .listen(3000)
```

We can access the web server by going to **http://localhost:3000**

By default, web browsers will send a GET method when visiting a page.

::: tip
Using the interactive browser above, hover on the blue highlight area to see different results between each path.
:::

## Path type

Paths in Elysia can be grouped into 3 types:

* **static paths** - static strings to locate the resource
* **dynamic paths** - segments can be any value
* **wildcards** - path until a specific point can be anything

You can use all of the path types together to compose a behavior for your web server.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/1', 'static path')
    .get('/id/:id', 'dynamic path')
    .get('/id/*', 'wildcard path')
    .listen(3000)
```

## Static Path

Static path is a hardcoded string to locate the resource on the server.

```ts
import { Elysia } from 'elysia'

new Elysia()
	.get('/hello', 'hello')
	.get('/hi', 'hi')
	.listen(3000)
```

## Dynamic path

Dynamic paths match some part and capture the value to extract extra information.

To define a dynamic path, we can use a colon `:` followed by a name.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id)
                      // ^?
    .listen(3000)
```

Here, a dynamic path is created with `/id/:id`, which tells Elysia to capture the value `:id` segment with values like **/id/1**, **/id/123**, **/id/anything**.

When requested, the server should return the response as follows:

| Path                   | Response  |
| ---------------------- | --------- |
| /id/1                  | 1         |
| /id/123                | 123       |
| /id/anything           | anything  |
| /id/anything?name=salt | anything  |
| /id                    | Not Found |
| /id/anything/rest      | Not Found |

Dynamic paths are great to include things like IDs that can be used later.

We refer to the named variable path as **path parameter** or **params** for short.

### Multiple path parameters

You can have as many path parameters as you like, which will then be stored into a `params` object.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id)
    .get('/id/:id/:name', ({ params: { id, name } }) => id + ' ' + name)
                             // ^?
    .listen(3000)
```

The server will respond as follows:

| Path                   | Response      |
| ---------------------- | ------------- |
| /id/1                  | 1             |
| /id/123                | 123           |
| /id/anything           | anything      |
| /id/anything?name=salt | anything      |
| /id                    | Not Found     |
| /id/anything/rest      | anything rest |

## Optional path parameters

Sometimes we might want a static and dynamic path to resolve the same handler.

We can make a path parameter optional by adding a question mark `?` after the parameter name.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id?', ({ params: { id } }) => `id ${id}`)
                          // ^?
    .listen(3000)
```

## Wildcards

Dynamic paths allow capturing a single segment while wildcards allow capturing the rest of the path.

To define a wildcard, we can use an asterisk `*`.

```typescript twoslash
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/*', ({ params }) => params['*'])
                    // ^?
    .listen(3000)
```

## Path priority

Elysia has path priorities as follows:

1. static paths
2. dynamic paths
3. wildcards

If both a static and a dynamic path are present, Elysia will resolve the static path rather than the dynamic path.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/1', 'static path')
    .get('/id/:id', 'dynamic path')
    .get('/id/*', 'wildcard path')
    .listen(3000)
```

## HTTP Verb

HTTP defines a set of request methods to indicate the desired action to be performed for a given resource

There are several HTTP verbs, but the most common ones are:

### GET

Requests using GET should only retrieve data.

### POST

Submits a payload to the specified resource, often causing state changes or side effects.

### PUT

Replaces all current representations of the target resource using the request's payload.

### PATCH

Applies partial modifications to a resource.

### DELETE

Deletes the specified resource.

***

To handle each of the different verbs, Elysia has a built-in API for several HTTP verbs by default, similar to `Elysia.get`

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/', 'hello')
    .post('/hi', 'hi')
    .listen(3000)
```

The Elysia HTTP method accepts the following parameters:

* **path**: Pathname
* **function**: Function to respond to the client
* **hook**: Additional metadata

You can read more about the HTTP methods on [HTTP Request Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).

## Custom Method

We can accept custom HTTP Methods with `Elysia.route`.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
    .get('/get', 'hello')
    .post('/post', 'hi')
    .route('M-SEARCH', '/m-search', 'connect') // [!code ++]
    .listen(3000)
```

**Elysia.route** accepts the following:

* **method**: HTTP Verb
* **path**: Pathname
* **function**: Function to respond to the client
* **hook**: Additional metadata

::: tip
Based on [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231#section-4.1), HTTP Verb is case-sensitive.

It's recommended to use the UPPERCASE convention for defining a custom HTTP Verb with Elysia.
:::

### ALL method

Elysia provides an `Elysia.all` for handling any HTTP method for a specified path using the same API like **Elysia.get** and **Elysia.post**

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .all('/', 'hi')
    .listen(3000)
```

Any HTTP method that matches the path, will be handled as follows:
| Path | Method | Result |
| ---- | -------- | ------ |
| / | GET | hi |
| / | POST | hi |
| / | DELETE | hi |

## Handle

Most developers use REST clients like Postman, Insomnia or Hoppscotch to test their API.

However, Elysia can be programmatically tested using `Elysia.handle`.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
    .get('/', 'hello')
    .post('/hi', 'hi')
    .listen(3000)

app.handle(new Request('http://localhost/')).then(console.log)
```

**Elysia.handle** is a function to process an actual request sent to the server.

::: tip
Unlike unit test's mock, **you can expect it to behave like an actual request** sent to the server.

But also useful for simulating or creating unit tests.
:::

## Group

When creating a web server, you will often have multiple routes sharing the same prefix:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .post('/user/sign-in', 'Sign in')
    .post('/user/sign-up', 'Sign up')
    .post('/user/profile', 'Profile')
    .listen(3000)
```

This can be improved with `Elysia.group`, allowing us to apply prefixes to multiple routes at the same time by grouping them together:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .group('/user', (app) =>
        app
            .post('/sign-in', 'Sign in')
            .post('/sign-up', 'Sign up')
            .post('/profile', 'Profile')
    )
    .listen(3000)
```

This code behaves the same as our first example and should be structured as follows:

| Path          | Result  |
| ------------- | ------- |
| /user/sign-in | Sign in |
| /user/sign-up | Sign up |
| /user/profile | Profile |

`.group()` can also accept an optional guard parameter to reduce boilerplate of using groups and guards together:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .group(
        '/user',
        {
            body: t.Literal('Rikuhachima Aru')
        },
        (app) => app
            .post('/sign-in', 'Sign in')
            .post('/sign-up', 'Sign up')
            .post('/profile', 'Profile')
    )
    .listen(3000)
```

You may find more information about grouped guards in [scope](/essential/plugin.html#scope).

### Prefix

We can separate a group into a separate plugin instance to reduce nesting by providing a **prefix** to the constructor.

```typescript
import { Elysia } from 'elysia'

const users = new Elysia({ prefix: '/user' })
    .post('/sign-in', 'Sign in')
    .post('/sign-up', 'Sign up')
    .post('/profile', 'Profile')

new Elysia()
    .use(users)
    .get('/', 'hello world')
    .listen(3000)
```

---

---
url: 'https://elysiajs.com/plugins/server-timing.md'
---

# Server Timing Plugin

This plugin adds support for auditing performance bottlenecks with Server Timing API

Install with:

```bash
bun add @elysia/server-timing
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { serverTiming } from '@elysia/server-timing'

new Elysia()
    .use(serverTiming())
    .get('/', () => 'hello')
    .listen(3000)
```

Server Timing will then append the 'Server-Timing' header with log duration, function name, and detail for each life-cycle function.

To inspect, open browser developer tools > Network > \[Request made through Elysia server] > Timing.

![Developer tools showing Server Timing screenshot](/assets/server-timing.webp)

Now you can effortlessly audit the performance bottleneck of your server.

## Config

Below is a config which is accepted by the plugin

### enabled

@default `NODE_ENV !== 'production'`

Determine whether or not Server Timing should be enabled

### allow

@default `undefined`

A condition for whether server timing should be logged

### trace

@default `undefined`

Allow Server Timing to log specified life-cycle events:

Trace accepts objects of the following:

* request: capture duration from request
* parse: capture duration from parse
* transform: capture duration from transform
* beforeHandle: capture duration from beforeHandle
* handle: capture duration from the handle
* afterHandle: capture duration from afterHandle
* total: capture total duration from start to finish

## Pattern

Below you can find the common patterns to use the plugin.

* [Allow Condition](#allow-condition)

## Allow Condition

You may disable Server Timing on specific routes via `allow` property

```ts
import { Elysia } from 'elysia'
import { serverTiming } from '@elysia/server-timing'

new Elysia()
    .use(
        serverTiming({
            allow: ({ request }) => {
                return new URL(request.url).pathname !== '/no-trace'
            }
        })
    )
```

---

---
url: 'https://elysiajs.com/tutorial/patterns/standalone-schema.md'
---

# Standalone Schema

When we define a schema using Guard, the schema will be added to a route. But it will be **overridden** if the route provides a schema:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.guard({
		body: t.Object({
			age: t.Number()
		})
	})
	.post(
		'/user',
		({ body }) => body,
		{
			// This will override the guard schema
			body: t.Object({
				name: t.String()
			})
		}
	)
	.listen(3000)
```

If we want a schema to **co-exist** with route schema, we can define it as **standalone schema**:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.guard({
		schema: 'standalone', // [!code ++]
		body: t.Object({
			age: t.Number()
		})
	})
	.post(
		'/user',
		// body will have both age and name property
		({ body }) => body,
		{
			body: t.Object({
				name: t.String()
			})
		}
	)
	.listen(3000)
```

## Schema Library Interoperability

Schemas between standalone schemas can be from different validation libraries.

For example you can define a standalone schema using **zod**, and a local schema using **Elysia.t**, and both will works interchangeably.

## Assignment

Let's make both `age` and `name` properties required in the request body by using standalone schema.

\<template #answer>

We can define a standalone schema by adding `schema: 'standalone'` in the guard options.

```typescript
import { Elysia, t } from 'elysia'
import { z } from 'zod'

new Elysia()
	.guard({
		schema: 'standalone', // [!code ++]
		body: z.object({
			age: z.number()
		})
	})
	.post(
		'/user',
		({ body }) => body,
		{
			body: t.Object({
				name: t.String()
			})
		}
	)
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/plugins/static.md'
---

# Static Plugin

This plugin can serve static files/folders for Elysia Server

Install with:

```bash
bun add @elysia/static
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { staticPlugin } from '@elysia/static'

new Elysia()
    .use(staticPlugin())
    .listen(3000)
```

By default, the static plugin default folder is `public`, and registered with `/public` prefix.

Suppose your project structure is:

```
| - src
  | - index.ts
| - public
  | - takodachi.png
  | - nested
    | - takodachi.png
```

The available path will become:

* /public/takodachi.png
* /public/nested/takodachi.png

## Config

Below is a config which is accepted by the plugin

### assets

@default `"public"`

Path to the folder to expose as static

### prefix

@default `"/public"`

Path prefix to register public files

### ignorePatterns

@default `[]`

List of files to ignore from serving as static files

### staticLimit

@default `1024`

By default, the static plugin will register paths to the Router with a static name, if the limits are exceeded, paths will be lazily added to the Router to reduce memory usage.
Tradeoff memory with performance.

### alwaysStatic

@default `false`

If set to true, static files path will be registered to Router skipping the `staticLimits`.

### headers

@default `{}`

Set response headers of files

### indexHTML

@default `false`

If set to true, the `index.html` file from the static directory will be served for any request that matches neither a route nor any existing static file.

## Pattern

Below you can find the common patterns to use the plugin.

* [Single File](#single-file)

## Single file

Suppose you want to return just a single file, you can use `file` instead of using the static plugin

```typescript
import { Elysia, file } from 'elysia'

new Elysia()
    .get('/file', file('public/takodachi.png'))
```

---

---
url: 'https://elysiajs.com/tutorial/getting-started/status-and-headers.md'
---

# Status

A status code is an indicator of how the server handles the request.

You must have heard of the infamous **404 Not Found** when you visit a non-existing page.

That's a **status code**.

By default, Elysia will return **200 OK** for a successful request.

Elysia also returns many other status codes depending on the situation like:

* 400 Bad Request
* 422 Unprocessable Entity
* 500 Internal Server Error

You can also return a status code by returning your response using the `status` function.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ status }) => status(418, "I'm a teapot"))
	.listen(3000)
```

The status code can be a number or a string status name. These are equivalent:

```typescript
status(418, "I'm a teapot")
status("I'm a teapot", "I'm a teapot")
```

String status names provide TypeScript autocompletion for all valid HTTP statuses.

See Status.

## Redirect

Similarly, you can also redirect the request to another URL by returning the `redirect` function.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ redirect }) => redirect('https://elysiajs.com'))
	.listen(3000)
```

See Redirect.

## Headers

Unlike status code and redirect, which you can return directly, you might need to set headers multiple times in your application.

That's why instead of returning a `headers` function, Elysia provides a `set.headers` object to set headers.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ set }) => {
		set.headers['x-powered-by'] = 'Elysia'

		return 'Hello World'
	})
	.listen(3000)
```

Because `headers` represents **request headers**, Elysia distinguishes between request headers and response headers by prefixing **set.headers** for response.

See Headers.

## Assignment

Let's exercise what we have learned.

\<template #answer>

1. To set status code to `418 I'm a teapot`, we can use `status` function.
2. To redirect `/docs` to `https://elysiajs.com`, we can use `redirect` function.
3. To set a custom header `x-powered-by` to `Elysia`, we can use `set.headers` object.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', ({ status, set }) => {
		set.headers['x-powered-by'] = 'Elysia'

		return status(418, 'Hello Elysia!')
	})
	.get('/docs', ({ redirect }) => redirect('https://elysiajs.com'))
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/plugins/swagger.md'
---

::: warning
Swagger plugin is deprecated and is no longer maintained. Please use [OpenAPI plugin](/plugins/openapi) instead.
:::

# Swagger Plugin

This plugin generates a Swagger endpoint for an Elysia server

Install with:

```bash
bun add @elysia/swagger
```

Then use it:

```typescript
import { Elysia } from 'elysia'
import { swagger } from '@elysia/swagger'

new Elysia()
    .use(swagger())
    .get('/', () => 'hi')
    .post('/hello', () => 'world')
    .listen(3000)
```

Accessing `/swagger` would show you a Scalar UI with the generated endpoint documentation from the Elysia server. You can also access the raw OpenAPI spec at `/swagger/json`.

## Config

Below is a config which is accepted by the plugin

### provider

@default `scalar`

UI Provider for documentation. Defaults to Scalar.

### scalar

Configuration for customizing Scalar.

Please refer to the [Scalar config](https://github.com/scalar/scalar/blob/main/documentation/configuration.md)

### swagger

Configuration for customizing Swagger.

Please refer to the [Swagger specification](https://swagger.io/specification/v2/).

### excludeStaticFile

@default `true`

Determine if Swagger should exclude static files.

### path

@default `/swagger`

Endpoint to expose Swagger

### exclude

Paths to exclude from Swagger documentation.

Value can be one of the following:

* **string**
* **RegExp**
* **Array\<string | RegExp>**

## Pattern

Below you can find the common patterns to use the plugin.

## Change Swagger Endpoint

You can change the swagger endpoint by setting [path](#path) in the plugin config.

```typescript
import { Elysia } from 'elysia'
import { swagger } from '@elysia/swagger'

new Elysia()
    .use(
        swagger({
            path: '/v2/swagger'
        })
    )
    .listen(3000)
```

## Customize Swagger info

```typescript
import { Elysia } from 'elysia'
import { swagger } from '@elysia/swagger'

new Elysia()
    .use(
        swagger({
            documentation: {
                info: {
                    title: 'Elysia Documentation',
                    version: '1.0.0'
                }
            }
        })
    )
    .listen(3000)
```

## Using Tags

Elysia can separate the endpoints into groups by using the Swagger tag system

First, define the available tags in the Swagger config object

```typescript
app.use(
    swagger({
        documentation: {
            tags: [
                { name: 'App', description: 'General endpoints' },
                { name: 'Auth', description: 'Authentication endpoints' }
            ]
        }
    })
)
```

Then use the detail property of the endpoint configuration section to assign that endpoint to the group

```typescript
app.get('/', () => 'Hello Elysia', {
    detail: {
        tags: ['App']
    }
})

app.group('/auth', (app) =>
    app.post(
        '/sign-up',
        async ({ body }) =>
            db.user.create({
                data: body,
                select: {
                    id: true,
                    username: true
                }
            }),
        {
            detail: {
                tags: ['Auth']
            }
        }
    )
)
```

This will produce a Swagger page as follows


## Security Configuration

To secure your API endpoints, you can define security schemes in the Swagger configuration. The example below demonstrates how to use Bearer Authentication (JWT) to protect your endpoints:

```typescript
app.use(
    swagger({
        documentation: {
            components: {
                securitySchemes: {
                    bearerAuth: {
                        type: 'http',
                        scheme: 'bearer',
                        bearerFormat: 'JWT'
                    }
                }
            }
        }
    })
)

export const addressController = new Elysia({
    prefix: '/address',
    detail: {
        tags: ['Address'],
        security: [
            {
                bearerAuth: []
            }
        ]
    }
})
```

This configuration ensures that all endpoints under the `/address` prefix require a valid JWT token for access.

---

---
url: 'https://elysiajs.com/patterns/unit-test.md'
---

# Unit Test&#x20;

Being WinterTC compliant, we can use Request / Response classes to test an Elysia server.

Elysia provides the **Elysia.handle** method, which accepts a Web Standard [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) and returns [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response), simulating an HTTP Request.

Bun includes a built-in [test runner](https://bun.sh/docs/cli/test) that offers a Jest-like API through the `bun:test` module, facilitating the creation of unit tests.

Create **test/index.test.ts** in the root of the project directory with the following:

```typescript
// test/index.test.ts
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'

describe('Elysia', () => {
    it('returns a response', async () => {
        const app = new Elysia().get('/', () => 'hi')

        const response = await app
            .handle(new Request('http://localhost/'))
            .then((res) => res.text())

        expect(response).toBe('hi')
    })
})
```

Then we can perform tests by running **bun test**

```bash
bun test
```

New requests to an Elysia server must be a fully valid URL, **NOT** a part of a URL.

The request must provide the URL as follows:

| URL                   | Valid |
| --------------------- | ----- |
| http://localhost/user | ✅    |
| /user                 | ❌    |

We can also use other testing libraries like Jest to create Elysia unit tests.

## Eden Treaty test

We may use Eden Treaty to create an end-to-end type safety test for Elysia server as follows:

```typescript twoslash
// test/index.test.ts
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'
import { treaty } from '@elysia/eden'

const app = new Elysia().get('/hello', 'hi')

const api = treaty(app)

describe('Elysia', () => {
    it('returns a response', async () => {
        const { data, error } = await api.hello.get()

        expect(data).toBe('hi')
              // ^?
    })
})
```

See [Eden Treaty Unit Test](/eden/treaty/unit-test) for setup and more information.

---

---
url: 'https://elysiajs.com/patterns/trace.md'
---

# Trace

Performance is an important aspect for Elysia.

We don't want to be fast for benchmarking purposes, we want you to have a really fast server in a real-world scenario.

There are many factors that can slow down our app - and it's hard to identify them, but **trace** can help solve that problem by injecting start and stop code to each life-cycle.

Trace allows us to inject code before and after each life-cycle event, block and interact with the execution of the function.

::: warning
trace doesn't work with dynamic mode `aot: false`, as it requires the function to be static and known at compile time otherwise it will have a large performance impact.
:::

## Trace

Trace uses a callback listener to ensure that callback function is finished before moving on to the next lifecycle event.

To use `trace`, you need to call `trace` method on the Elysia instance, and pass a callback function that will be executed for each life-cycle event.

You may listen to each lifecycle by adding `on` prefix followed by the lifecycle name, for example `onHandle` to listen to the `handle` event.

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
    .trace(async ({ onHandle }) => {
	    onHandle(({ begin, onStop }) => {
			onStop(({ end }) => {
        		console.log('handle took', end - begin, 'ms')
			})
	    })
    })
    .get('/', () => 'Hi')
    .listen(3000)
```

Please refer to [Life Cycle Events](/essential/life-cycle#events) for more information:

![Elysia Life Cycle](/assets/lifecycle-chart.svg)

## Children

Every event except `handle` has children, which is an array of events that are executed inside for each lifecycle event.

You can use `onEvent` to listen to each child event in order

```ts
import { Elysia } from 'elysia'

const sleep = (time = 1000) =>
    new Promise((resolve) => setTimeout(resolve, time))

const app = new Elysia()
    .trace(async ({ onBeforeHandle }) => {
        onBeforeHandle(({ total, onEvent }) => {
            console.log('total children:', total)

            onEvent(({ onStop }) => {
                onStop(({ elapsed }) => {
                    console.log('child took', elapsed, 'ms')
                })
            })
        })
    })
    .get('/', () => 'Hi', {
        beforeHandle: [
            function setup() {},
            async function delay() {
                await sleep()
            }
        ]
    })
    .listen(3000)
```

In this example, total children will be `2` because there are 2 children in the `beforeHandle` event.

Then we listen to each child event by using `onEvent` and print the duration of each child event.

## Trace Parameter

When each lifecycle is called

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
	// This is trace parameter
	// hover to view the type
	.trace((parameter) => {
	})
	.get('/', () => 'Hi')
	.listen(3000)
```

`trace` accepts the following parameters:

### id - `number`

Randomly generated unique ID for each request

### context - `Context`

Elysia's [Context](/essential/handler.html#context), eg. `set`, `store`, `query`, `params`

### set - `Context.set`

Shortcut for `context.set`, to set a headers or status of the context

### store - `Singleton.store`

Shortcut for `context.store`, to access a data in the context

### time - `number`

Timestamp of when request is called

### on\[Event] - `TraceListener`

An event listener for each life-cycle event.

You may listen to the following life-cycle:

* **onRequest** - get notified of every new request
* **onParse** - array of functions to parse the body
* **onTransform** - transform request and context before validation
* **onBeforeHandle** - custom requirement to check before the main handler, can skip the main handler if response returned.
* **onHandle** - function assigned to the path
* **onAfterHandle** - interact with the response before sending it back to the client
* **onMapResponse** - map returned value into a Web Standard Response
* **onError** - handle error thrown during processing request
* **onAfterResponse** - cleanup function after response is sent

## Trace Listener

A listener for each life-cycle event

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
	.trace(({ onBeforeHandle }) => {
		// This is trace listener
		// hover to view the type
		onBeforeHandle((parameter) => {

		})
	})
	.get('/', () => 'Hi')
	.listen(3000)
```

Each lifecycle listener accepts the following

### name - `string`

The name of the function, if the function is anonymous, the name will be `anonymous`

### begin - `number`

The time when the function is started

### end - `Promise<number>`

The time when the function is ended, will be resolved when the function is ended

### error - `Promise<Error | null>`

Error that was thrown in the lifecycle, will be resolved when the function is ended

### onStop - `callback?: (detail: TraceEndDetail) => any`

A callback that will be executed when the lifecycle is ended

```ts
import { Elysia } from 'elysia'

const app = new Elysia()
	.trace(({ onBeforeHandle, set }) => {
		onBeforeHandle(({ onStop }) => {
			onStop(({ elapsed }) => {
				set.headers['X-Elapsed'] = elapsed.toString()
			})
		})
	})
	.get('/', () => 'Hi')
	.listen(3000)
```

It's recommended to mutate context in this function as there's a lock mechanism to ensure the context is mutated successfully before moving on to the next lifecycle event

## TraceEndDetail

A parameter that passed to `onStop` callback

### end - `number`

The time when the function is ended

### error - `Error | null`

Error that was thrown in the lifecycle

### elapsed - `number`

Elapsed time of the lifecycle or `end - begin`

---

---
url: 'https://elysiajs.com/patterns/typebox.md'
---

# TypeBox (Elysia.t)

Here's common patterns for writing validation types using `Elysia.t`.

## Primitive Type

The TypeBox API is designed around and is similar to TypeScript types.

There are many familiar names and behaviors that intersect with TypeScript counterparts, such as **String**, **Number**, **Boolean**, and **Object**, as well as more advanced features like **Intersect**, **KeyOf**, and **Tuple** for versatility.

If you are familiar with TypeScript, creating a TypeBox schema behaves the same as writing a TypeScript type, except it provides actual type validation at runtime.

To create your first schema, import **Elysia.t** from Elysia and start with the most basic type:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/', ({ body }) => `Hello ${body}`, {
		body: t.String()
	})
	.listen(3000)
```

This code tells Elysia to validate an incoming HTTP body, ensuring that the body is a string. If it is a string, it will be allowed to flow through the request pipeline and handler.

If the shape doesn't match, it will throw an error into the [Error Life Cycle](/essential/life-cycle.html#on-error).

![Elysia Life Cycle](/assets/lifecycle-chart.svg)

### Basic Type

TypeBox provides basic primitive types with the same behavior as TypeScript types.

The following table lists the most common basic types:

```typescript
t.String()
```

```typescript
string
```

```typescript
t.Number()
```

```typescript
number
```

```typescript
t.Boolean()
```

```typescript
boolean
```

```typescript
t.Array(
    t.Number()
)
```

```typescript
number[]
```

```typescript
t.Object({
    x: t.Number()
})
```

```typescript
{
    x: number
}
```

```typescript
t.Null()
```

```typescript
null
```

```typescript
t.Literal(42)
```

```typescript
42
```

Elysia extends all types from TypeBox, allowing you to reference most of the API from TypeBox for use in Elysia.

See [TypeBox's Type](https://github.com/sinclairzx81/typebox#json-types) for additional types supported by TypeBox.

### Attribute

TypeBox can accept arguments for more comprehensive behavior based on the JSON Schema 7 specification.

```typescript
t.String({
    format: 'email'
})
```

```typescript
saltyaom@elysia.com
```

```typescript
t.Number({
    minimum: 10,
    maximum: 100
})
```

```typescript
10
```

```typescript
t.Array(
    t.Number(),
    {
        /**
         * Minimum number of items
         */
        minItems: 1,
        /**
         * Maximum number of items
         */
        maxItems: 5
    }
)
```

```typescript
[1, 2, 3, 4, 5]
```

```typescript
t.Object(
    {
        x: t.Number()
    },
    {
        /**
         * @default false
         * Accept additional properties
         * that not specified in schema
         * but still match the type
         */
        additionalProperties: true
    }
)
```

```typescript
x: 100
y: 200
```

See [JSON Schema 7 specification](https://json-schema.org/draft/2020-12/json-schema-validation) for more explanation of each attribute.

## Honorable Mentions

The following are common patterns often found useful when creating a schema.

### Union

Allows a field in `t.Object` to have multiple types.

```typescript
t.Union([
    t.String(),
    t.Number()
])
```

```typescript
string | number
```

```
Hello
123
```

### Optional

Allows a field in `t.Object` to be undefined or optional.

```typescript
t.Object({
    x: t.Number(),
    y: t.Optional(t.Number())
})
```

```typescript
{
    x: number,
    y?: number
}
```

```typescript
{
    x: 123
}
```

### Partial

Allows all fields in `t.Object` to be optional.

```typescript
t.Partial(
    t.Object({
        x: t.Number(),
        y: t.Number()
    })
)
```

```typescript
{
    x?: number,
    y?: number
}
```

```typescript
{
    y: 123
}
```

## Elysia Type

`Elysia.t` is based on TypeBox with pre-configuration for server usage, providing additional types commonly found in server-side validation.

You can find all the source code for Elysia types in `elysia/type-system`.

The following are types provided by Elysia:

### UnionEnum

`UnionEnum` allows the value to be one of the specified values.

```typescript
t.UnionEnum(['rapi', 'anis', 1, true, false])
```

### File

A singular file, often useful for **file upload** validation.

```typescript
t.File()
```

File extends the attributes of the base schema, with additional properties as follows:

#### type

Specifies the format of the file, such as image, video, or audio.

If an array is provided, it will attempt to validate if any of the formats are valid.

```typescript
type?: MaybeArray<string>
```

#### minSize

Minimum size of the file.

Accepts a number in bytes or a suffix of file units:

```typescript
minSize?: number | `${number}${'k' | 'm'}`
```

#### maxSize

Maximum size of the file.

Accepts a number in bytes or a suffix of file units:

```typescript
maxSize?: number | `${number}${'k' | 'm'}`
```

#### File Unit Suffix:

The following are the specifications of the file unit:
m: MegaByte (1048576 byte)
k: KiloByte (1024 byte)

### Files

Extends from [File](#file), but adds support for an array of files in a single field.

```typescript
t.Files()
```

Files extends the attributes of the base schema, array, and File.

### Cookie

Object-like representation of a Cookie Jar extended from the Object type.

```typescript
t.Cookie({
    name: t.String()
})
```

Cookie extends the attributes of [Object](https://json-schema.org/draft/2020-12/json-schema-validation#name-validation-keywords-for-obj) and [Cookie](https://github.com/jshttp/cookie#options-1) with additional properties as follows:

#### secrets

The secret key for signing cookies.

Accepts a string or an array of strings.

```typescript
secrets?: string | string[]
```

If an array is provided, [Key Rotation](https://crypto.stackexchange.com/questions/41796/whats-the-purpose-of-key-rotation) will be used. The newly signed value will use the first secret as the key.

### Nullable

Allows the value to be null but not undefined.

```typescript
t.Nullable(t.String())
```

### MaybeEmpty

Allows the value to be null and undefined.

```typescript
t.MaybeEmpty(t.String())
```

For additional information, you can find the full source code of the type system in [`elysia/type-system`](https://github.com/elysiajs/elysia/blob/main/src/type-system/index.ts).

### Form

A syntax sugar for our `t.Object` with support for verifying return value of [form](/essential/handler.html#formdata) (FormData).

```typescript
t.Form({
	someValue: t.File()
})
```

### UInt8Array

Accepts a buffer that can be parsed into a `Uint8Array`.

```typescript
t.UInt8Array()
```

This is useful when you want to accept a buffer that can be parsed into a `Uint8Array`, such as in a binary file upload. It's designed to use for the validation of body with `arrayBuffer` parser to enforce the body type.

### ArrayBuffer

Accepts a buffer that can be parsed into a `ArrayBuffer`.

```typescript
t.ArrayBuffer()
```

This is useful when you want to accept a buffer that can be parsed into a `Uint8Array`, such as in a binary file upload. It's designed to use for the validation of body with `arrayBuffer` parser to enforce the body type.

### ObjectString

Accepts a string that can be parsed into an object.

```typescript
t.ObjectString()
```

This is useful when you want to accept a string that can be parsed into an object but the environment does not allow it explicitly, such as in a query string, header, or FormData body.

### BooleanString

Accepts a string that can be parsed into a boolean.

Similar to [ObjectString](#objectstring), this is useful when you want to accept a string that can be parsed into a boolean but the environment does not allow it explicitly.

```typescript
t.BooleanString()
```

### Numeric

Numeric accepts a numeric string or number and then transforms the value into a number.

```typescript
t.Numeric()
```

This is useful when an incoming value is a numeric string, for example, a path parameter or query string.

Numeric accepts the same attributes as [Numeric Instance](https://json-schema.org/draft/2020-12/json-schema-validation#name-validation-keywords-for-num).

## Elysia behavior

Elysia uses TypeBox by default.

However, to help make handling HTTP easier. Elysia has some dedicated types and has some behavioral differences from TypeBox.

## Optional

To make a field optional, use `t.Optional`.

This will allow clients to optionally provide a query parameter. This behavior also applies to `body`, `headers`.

This is different from TypeBox where optional is to mark a field of an object as optional.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/optional', ({ query }) => query, {
		query: t.Optional(
			t.Object({
				name: t.String()
			})
		)
	})
```

## Number to Numeric

By default, Elysia will convert a `t.Number` to [t.Numeric](#numeric) when provided as route schema.

Because parsed HTTP headers, query, and URL parameters are always strings. This means that even if a value is a number, it will be treated as a string.

Elysia overrides this behavior by checking if a string value looks like a number then converting it appropriately.

This is only applied when it is used as a route schema and not in a nested `t.Object`.

```ts
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/:id', ({ id }) => id, {
		params: t.Object({
			// Converted to t.Numeric()
			id: t.Number()
		}),
		body: t.Object({
			// NOT converted to t.Numeric()
			id: t.Number()
		})
	})

// NOT converted to t.Numeric()
t.Number()
```

## Boolean to BooleanString

Similar to [Number to Numeric](#number-to-numeric)

Any `t.Boolean` will be converted to `t.BooleanString`.

```ts
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/:id', ({ id }) => id, {
		params: t.Object({
			// Converted to t.Boolean()
			id: t.Boolean()
		}),
		body: t.Object({
			// NOT converted to t.Boolean()
			id: t.Boolean()
		})
	})

// NOT converted to t.BooleanString()
t.Boolean()
```

---

---
url: 'https://elysiajs.com/patterns/typescript.md'
---

# TypeScript

Elysia has first-class support for TypeScript out of the box.

Most of the time, you wouldn't need to add any TypeScript annotations manually.

## Inference

Elysia infers the type of request and response based on the schema you provide.

```ts twoslash
import { Elysia, t } from 'elysia'
import { z } from 'zod'

const app = new Elysia()
  	.post('/user/:id', ({ body }) => body, {
  	//                     ^?
	  	body: t.Object({
			id: t.String()
		}),
		query: z.object({
			name: z.string()
		})
   	})
```

Elysia can automatically infer types from schema like TypeBox and [your favorite validation library](/essential/validation#standard-schema) like:

* Zod
* Valibot
* ArkType
* Effect Schema
* Yup
* Joi

### Schema to Type

All of schema library supported by Elysia can be converted to TypeScript type.

\<Tab
id="quickstart"
:names="\['TypeBox', 'Zod', 'Valibot', 'ArkType']"
:tabs="\['typebox', 'zod', 'valibot', 'arktype']"
noTitle

>

```ts twoslash
import { Elysia, t } from 'elysia'

const User = t.Object({
  	id: t.String(),
  	name: t.String()
})

type User = typeof User['static']
//    ^?
```

```ts twoslash
import { z } from 'zod'

const User = z.object({
  	id: z.string(),
  	name: z.string()
})

type User = z.infer<typeof User>
//    ^?
```

```ts twoslash
import * as v from 'valibot'

const User = v.object({
  	id: v.string(),
  	name: v.string()
})

type User = v.InferOutput<typeof User>
//    ^?
```

```ts twoslash
import { type } from 'arktype'

const User = type({
  	id: 'string',
  	name: 'string'
})

type User = typeof User.infer
//    ^?
```

## Type Performance

Elysia is built with type inference performance in mind.

Before every release, we have a local benchmark to ensure that type inference is always snappy, fast, and doesn't blow up your IDE with "Type instantiation is excessively deep and possibly infinite" error.

Most of the time writing Elysia, you wouldn't encounter any type performance issue.

However, if you do, here is how to break down what's slowing down your type inference:

1. Navigate to the root of your project and run

```
tsc --generateTrace trace --noEmit --incremental false
```

This should generate a `trace` folder in your project root.

2. Open [Perfetto UI](https://ui.perfetto.dev) and drag the `trace/trace.json` file

![Perfetto](/assets/perfetto.webp)

> It should show you a flame graph like this

Then you can find a chunk that takes a long time to be evaluated, click on it and it should show you how long the inference take, and which file, and line number it is coming from.

This should help you to identify the bottleneck of your type inference.

### Eden

If you are having a slow type inference issue when using [Eden](/eden/overview), you can try using a sub app of Elysia to isolate the type inference.

```ts [backend/src/index.ts]
import { Elysia } from 'elysia'
import { plugin1, plugin2, plugin3 } from './plugin'

const app = new Elysia()
	.use([plugin1, plugin2, plugin3])
  	.listen(3000)

export type app = typeof app

// Export sub app
export type subApp = typeof plugin1 // [!code ++]
```

And on your frontend, you can import the sub app instead of the whole app.

```ts [frontend/src/index.ts]
import { treaty } from '@elysia/eden'
import type { subApp } from 'backend/src'

const api = treaty<subApp>('localhost:3000') // [!code ++]
```

This should make your type inference faster as it doesn't need to evaluate the whole app.

See [Eden Treaty](/eden/overview) to learn more about Eden.

---

---
url: 'https://elysiajs.com/tutorial/features/unit-test.md'
---

# Unit Test

Elysia provides a **Elysia.fetch** function to easily test your application.

**Elysia.fetch** takes a Web Standard Request, and returns a Response similar to the browser's fetch API.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', 'Hello World')

app.fetch(new Request('http://localhost/'))
	.then((res) => res.text())
	.then(console.log)
```

This will run a request like an **actual request** (not simulated).

### Test

This allows us to easily test our application without running a server.

::: code-group

```typescript [Bun Test]
import { describe, it, expect } from 'bun:test'

import { Elysia } from 'elysia'

describe('Elysia', () => {
	it('should return Hello World', async () => {
		const app = new Elysia().get('/', 'Hello World')

		const text = await app.fetch(new Request('http://localhost/'))
			.then(res => res.text())

		expect(text).toBe('Hello World')
	})
})
```

```typescript [Vitest]
import { describe, it, expect } from 'vitest'

import { Elysia } from 'elysia'

describe('Elysia', () => {
	it('should return Hello World', async () => {
		const app = new Elysia().get('/', 'Hello World')

		const text = await app.fetch(new Request('http://localhost/'))
			.then(res => res.text())

		expect(text).toBe('Hello World')
	})
})
```

```typescript [Jest]
import { describe, it, test } from '@jest/globals'

import { Elysia } from 'elysia'

describe('Elysia', () => {
	test('should return Hello World', async () => {
		const app = new Elysia().get('/', 'Hello World')

		const text = await app.fetch(new Request('http://localhost/'))
			.then(res => res.text())

		expect(text).toBe('Hello World')
	})
})
```

:::

See Unit Test.

## Assignment

Let's click the  icon in the preview to see how's the request is logged.

---

---
url: 'https://elysiajs.com/tutorial/getting-started/validation.md'
---

# Validation

Elysia offers data validation out of the box.

You can use `Elysia.t` to define a schema.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post(
		'/user',
		({ body: { name } }) => `Hello ${name}!`,
		{
			body: t.Object({
				name: t.String(),
				age: t.Number()
			})
		}
	)
	.listen(3000)
```

When you define a schema, Elysia will ensure the data is in a correct shape.

If the data doesn't match the schema, Elysia will return a **422 Unprocessable Entity** error.

See Validation.

### Bring your own

Alternatively, Elysia support **Standard Schema**, allowing you to use a library of your choice like **zod**, **yup** or **valibot**.

```typescript
import { Elysia } from 'elysia'
import { z } from 'zod'

new Elysia()
	.post(
		'/user',
		({ body: { name } }) => `Hello ${name}!`,
		{
			body: z.object({
				name: z.string(),
				age: z.number()
			})
		}
	)
	.listen(3000)
```

See Standard Schema for all compatible schema.

## Validation Type

You can validate the following property:

* `body`
* `query`
* `params`
* `headers`
* `cookie`
* `response`

Once a schema is defined, Elysia will infer types for you so you don't have to define a separate schema in TypeScript.

See Schema Type for each type.

## Response Validation

When you define a validation schema for `response`, Elysia will validate the response before sending it to the client, and type check the response for you.

You can also specify which status code to validate:

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.get(
		'/user',
		() => `Hello Elysia!`,
		{
			response: {
				200: t.Literal('Hello Elysia!'),
				418: t.Object({
					message: t.Literal("I'm a teapot")
				})
			}
		}
	)
	.listen(3000)
```

See Response Validation.

## Assignment

Let's exercise what we have learned.

\<template #answer>

We can define a schema by using `t.Object` provided to the `body` property.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post(
		'/user',
		({ body: { name } }) => `Hello ${name}!`,
		{
			body: t.Object({
				name: t.String()
			})
		}
	)
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/essential/validation.md'
---

# Validation&#x20;

Elysia provides a schema to validate data out of the box to ensure that the data is in the correct format.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id, {
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
```

### TypeBox

**Elysia.t** is a schema builder based on [TypeBox](https://github.com/sinclairzx81/typebox) that provides type-safety at runtime, compile-time, and OpenAPI schema generation from a single source of truth.

Elysia tailors TypeBox for server-side validation for a seamless experience.

### Standard Schema

Elysia also supports [Standard Schema](https://github.com/standard-schema/standard-schema), allowing you to use your favorite validation library:

* Zod
* Valibot
* ArkType
* Effect Schema
* Yup
* Joi
* [and more](https://github.com/standard-schema/standard-schema)

To use Standard Schema, simply import the schema and provide it to the route handler.

```typescript twoslash
import { Elysia } from 'elysia'
import { z } from 'zod'
import * as v from 'valibot'

new Elysia()
	.get('/id/:id', ({ params: { id }, query: { name } }) => id, {
	//                           ^?
		params: z.object({
			id: z.coerce.number()
		}),
		query: v.object({
			name: v.literal('Lilith')
		})
	})
	.listen(3000)
```

You can use any validator together in the same handler without any issue.

## Schema type

Elysia supports declarative schemas with the following types:

***

These properties should be provided as the third argument of the route handler to validate the incoming request.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/id/:id', () => 'Hello World!', {
        query: t.Object({
            name: t.String()
        }),
        params: t.Object({
            id: t.Number()
        })
    })
    .listen(3000)
```

The response should be as follows:
| URL | Query | Params |
| --- | --------- | ------------ |
| /id/a | ❌ | ❌ |
| /id/1?name=Elysia | ✅ | ✅ |
| /id/1?alias=Elysia | ❌ | ✅ |
| /id/a?name=Elysia | ✅ | ❌ |
| /id/a?alias=Elysia | ❌ | ❌ |

When a schema is provided, the type will be inferred from the schema automatically and an OpenAPI type will be generated for API documentation, eliminating the redundant task of providing the type manually.

## Guard

Guard can be used to apply a schema to multiple handlers.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
    .get('/none', ({ query }) => 'hi')
                   // ^?

    .guard({ // [!code ++]
        query: t.Object({ // [!code ++]
            name: t.String() // [!code ++]
        }) // [!code ++]
    }) // [!code ++]
    .get('/query', ({ query }) => query)
                    // ^?
    .listen(3000)
```

This code ensures that the query must have **name** with a string value for every handler after it. The response should be listed as follows:

The response should be listed as follows:

| Path          | Response |
| ------------- | -------- |
| /none         | hi       |
| /none?name=a  | hi       |
| /query        | error    |
| /query?name=a | a        |

If multiple global schemas are defined for the same property, the latest one will take precedence. If both local and global schemas are defined, the local one will take precedence.

### Guard Schema Type

Guard supports 2 types to define a validation.

### **override (default)**

Override schemas if they collide with each other.

![Elysia run with default override guard showing schema gets override](/blog/elysia-13/schema-override.webp)

### **standalone**&#x20;

Separate collided schemas, and run both independently resulting in both being validated.

![Elysia run with standalone merging multiple guard together](/blog/elysia-13/schema-standalone.webp)

To define schema type of guard with `schema`:

```ts
import { Elysia } from 'elysia'

new Elysia()
	.guard({
		schema: 'standalone', // [!code ++]
		response: t.Object({
			title: t.String()
		})
	})
```

## Body

An [HTTP message](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages) is data sent to the server. It can be in the form of JSON, form-data, or any other format.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/body', ({ body }) => body, {
                    // ^?




		body: t.Object({
			name: t.String()
		})
	})
	.listen(3000)
```

The validation should be as follows:
| Body | Validation |
| --- | --------- |
| { name: 'Elysia' } | ✅ |
| { name: 1 } | ❌ |
| { alias: 'Elysia' } | ❌ |
| `undefined` | ❌ |

Elysia disables body-parser for **GET** and **HEAD** messages by default, following the specs of HTTP/1.1 [RFC2616](https://www.rfc-editor.org/rfc/rfc2616#section-4.3)

> If the request method does not include defined semantics for an entity-body, then the message-body SHOULD be ignored when handling the request.

Most browsers disable the attachment of the body by default for **GET** and **HEAD** methods.

#### Specs

Validate an incoming [HTTP Message](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages) (or body).

These are additional messages for the web server to process.

The body is provided in the same way as the `body` in `fetch` API. The content type should be set accordingly to the defined body.

```typescript
fetch('https://elysiajs.com', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Elysia'
    })
})
```

### File

File is a special type of body that can be used to upload files.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/body', ({ body }) => body, {
                    // ^?





		body: t.Object({
			file: t.File({ format: 'image/*' }),
			multipleFiles: t.Files()
		})
	})
	.listen(3000)
```

By providing a file type, Elysia will automatically assume that the content-type is `multipart/form-data`.

### File (Standard Schema)

If you're using Standard Schema, it's important to note that Elysia will not be able to validate content type automatically similar to `t.File`.

But Elysia export a `fileType` that can be used to validate file type by using magic number.

```typescript
import { Elysia, fileType } from 'elysia'
import { z } from 'zod'

new Elysia()
	.post('/body', ({ body }) => body, {
		body: z.object({
			file: z.file().refine((file) => fileType(file, 'image/jpeg')) // [!code ++]
		})
	})
```

It's very important that you **should use the `fileType` utility to** validate the file type as **most validators don't actually validate the file** correctly, like checking the content type value which can lead to security vulnerabilities.

## Query

Query is the data sent through the URL. It can be in the form of `?key=value`.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/query', ({ query }) => query, {
                    // ^?




		query: t.Object({
			name: t.String()
		})
	})
	.listen(3000)
```

Query must be provided in the form of an object.

The validation should be as follows:
| Query | Validation |
| ---- | --------- |
| /?name=Elysia | ✅ |
| /?name=1 | ✅ |
| /?alias=Elysia | ❌ |
| /?name=ElysiaJS\&alias=Elysia | ✅ |
| / | ❌ |

#### Specs

A query string is part of the URL that starts with **?** and can contain one or more query parameters, which are key-value pairs used to convey additional information to the server, usually for customized behavior like filtering or searching.

![URL Object](/essential/url-object.svg)

Query is provided after the **?** in Fetch API.

```typescript
fetch('https://elysiajs.com/?name=Elysia')
```

When specifying query parameters, it's crucial to understand that all query parameter values are represented as strings. This is due to how they are encoded and appended to the URL.

### Coercion

Elysia will coerce applicable schema on `query` to respective type automatically.

See [Elysia behavior](/patterns/type#elysia-behavior) for more information.

```ts twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/', ({ query }) => query, {
               // ^?




		query: t.Object({ // [!code ++]
			id: t.Number() // [!code ++]
		}) // [!code ++]
	})
	.listen(3000)
```

### Array

By default, Elysia treats query parameters as a single string even if specified multiple times.

To use arrays, we need to explicitly declare them as arrays.

```ts twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/', ({ query }) => query, {
               // ^?




		query: t.Object({
			name: t.Array(t.String()) // [!code ++]
		})
	})
	.listen(3000)
```

Once Elysia detect that a property is assignable to array, Elysia will coerce it to an array of the specified type.

By default, Elysia format query array with the following format:

#### nuqs

This format is used by [nuqs](https://nuqs.47ng.com).

By using **,** as a delimiter, a property will be treated as array.

```
http://localhost?name=rapi,anis,neon&squad=counter
{
	name: ['rapi', 'anis', 'neon'],
	squad: 'counter'
}
```

#### HTML form format

If a key is assigned multiple times, the key will be treated as an array.

This is similar to HTML form format when an input with the same name is specified multiple times.

```
http://localhost?name=rapi&name=anis&name=neon&squad=counter
// name: ['rapi', 'anis', 'neon']
```

## Params

Params or path parameters are the data sent through the URL path.

They can be in the form of `/key`.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/id/:id', ({ params }) => params, {
                      // ^?




		params: t.Object({
			id: t.Number()
		})
	})
```

Params must be provided in the form of an object.

The validation should be as follows:
| URL | Validation |
| --- | --------- |
| /id/1 | ✅ |
| /id/a | ❌ |

#### Specs

Path parameters (not to be confused with query string or query parameter).

**This is usually not needed as Elysia can infer types from path parameters automatically**, unless there is a need for a specific value pattern, such as a numeric value or template literal pattern.

```typescript
fetch('https://elysiajs.com/id/1')
```

### Params type inference

If a params schema is not provided, Elysia will automatically infer the type as a string.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/id/:id', ({ params }) => params)
                      // ^?
```

## Headers

Headers are the data sent through the request's header.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/headers', ({ headers }) => headers, {
                      // ^?




		headers: t.Object({
			authorization: t.String()
		})
	})
```

Unlike other types, headers have `additionalProperties` set to `true` by default.

This means that headers can have any key-value pair, but the value must match the schema.

#### Specs

HTTP headers let the client and the server pass additional information with an HTTP request or response, usually treated as metadata.

This field is usually used to enforce some specific header fields, for example, `Authorization`.

Headers are provided in the same way as the `body` in `fetch` API.

```typescript
fetch('https://elysiajs.com/', {
    headers: {
        authorization: 'Bearer 12345'
    }
})
```

::: tip
Elysia will parse headers as lower-case keys only.

Please make sure that you are using lower-case field names when using header validation.
:::

## Cookie

Cookie is the data sent through the request's cookie.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/cookie', ({ cookie }) => cookie, {
                     // ^?



		cookie: t.Cookie({
			cookieName: t.String()
		})
	})
```

Cookies must be provided in the form of `t.Cookie` or `t.Object`.

Same as `headers`, cookies have `additionalProperties` set to `true` by default.

#### Specs

An HTTP cookie is a small piece of data that a server sends to the client. It's data sent with every visit to the same web server to let the server remember client information.

In simpler terms, it's a stringified state that is sent with every request.

This field is usually used to enforce some specific cookie fields.

A cookie is a special header field that the Fetch API doesn't accept a custom value for but is managed by the browser. To send a cookie, you must use a `credentials` field instead:

```typescript
fetch('https://elysiajs.com/', {
    credentials: 'include'
})
```

### t.Cookie

`t.Cookie` is a special type that is equivalent to `t.Object` but allows to set cookie-specific options.

```typescript twoslash
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/cookie', ({ cookie }) => cookie.name.value, {
                      // ^?




		cookie: t.Cookie({
			name: t.String()
		}, {
			secure: true,
			httpOnly: true
		})
	})
```

## Response

Response is the data returned from the handler.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/response', () => {
		return {
			name: 'Jane Doe'
		}
	}, {
		response: t.Object({
			name: t.String()
		})
	})
```

### Response per status

Responses can be set per status code.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.get('/response', ({ status }) => {
		if (Math.random() > 0.5)
			return status(400, {
				error: 'Something went wrong'
			})

		return {
			name: 'Jane Doe'
		}
	}, {
		response: {
			200: t.Object({
				name: t.String()
			}),
			400: t.Object({
				error: t.String()
			})
		}
	})
```

This is an Elysia-specific feature, allowing us to make a field optional.

## Error Provider

There are two ways to provide a custom error message when the validation fails:

1. Inline `status` property
2. Using [onError](/essential/life-cycle.html#on-error) event

### Error Property

Elysia offers an additional **error** property, allowing us to return a custom error message if the field is invalid.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .post('/', () => 'Hello World!', {
        body: t.Object({
            x: t.Number({
               	error: 'x must be a number'
            })
        })
    })
    .listen(3000)
```

The following is an example of using the error property on various types:

```typescript
t.String({
    format: 'email',
    error: 'Invalid email :('
})
```

```
Invalid Email :(
```

```typescript
t.Array(
    t.String(),
    {
        error: 'All members must be a string'
    }
)
```

```
All members must be a string
```

```typescript
t.Object({
    x: t.Number()
}, {
    error: 'Invalid object UnU'
})
```

```
Invalid object UnU
```

```typescript
t.Object({
    x: t.Number({
        error({ errors, type, validation, value }) {
            return 'Expected x to be a number'
        }
    })
})
```

```
Expected x to be a number
```

## Custom Error

TypeBox offers an additional "**error**" property, allowing us to return a custom error message if the field is invalid.

```typescript
t.String({
    format: 'email',
    error: 'Invalid email :('
})
```

```
Invalid Email :(
```

```typescript
t.Object({
    x: t.Number()
}, {
    error: 'Invalid object UnU'
})
```

```
Invalid object UnU
```

### Error message as function

In addition to a string, Elysia type's error can also accept a function to programmatically return a custom error for each property.

The error function accepts the same arguments as `ValidationError`

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .post('/', () => 'Hello World!', {
        body: t.Object({
            x: t.Number({
                error() {
                    return 'Expected x to be a number'
                }
            })
        })
    })
    .listen(3000)
```

::: tip
Hover over the `error` to see the type.
:::

### Error is Called Per Field

Please note that the error function will only be called if the field is invalid.

Please consider the following table:

```typescript
t.Object({
    x: t.Number({
        error() {
            return 'Expected x to be a number'
        }
    })
})
```

```json
{
    x: "hello"
}
```

```typescript
t.Object({
    x: t.Number({
        error() {
            return 'Expected x to be a number'
        }
    })
})
```

```json
"hello"
```

```typescript
t.Object(
    {
        x: t.Number({
            error() {
                return 'Expected x to be a number'
            }
        })
    }, {
        error() {
            return 'Expected value to be an object'
        }
    }
)
```

```json
"hello"
```

### onError

We can customize the behavior of validation based on the [onError](/essential/life-cycle.html#on-error) event by narrowing down the error code to "**VALIDATION**".

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.onError(({ code, error }) => {
		if (code === 'VALIDATION')
		    return error.message
	})
	.listen(3000)
```

The narrowed-down error type will be typed as `ValidationError` imported from **elysia/error**.

**ValidationError** exposes a property named **validator**, typed as [TypeCheck](https://github.com/sinclairzx81/typebox#typecheck), allowing us to interact with TypeBox functionality out of the box.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
    .onError(({ code, error }) => {
        if (code === 'VALIDATION')
            return error.all[0].message
    })
    .listen(3000)
```

### Error List

**ValidationError** provides a method `ValidationError.all`, allowing us to list all of the error causes.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post('/', ({ body }) => body, {
		body: t.Object({
			name: t.String(),
			age: t.Number()
		}),
		error({ code, error }) {
			switch (code) {
				case 'VALIDATION':
                    console.log(error.all)

                    // Find a specific error name (path is OpenAPI Schema compliance)
                    const name = error.all.find(
						(x) => x.summary && x.path === '/name'
					)

                    // If there is a validation error, then log it
                    if(name)
    					console.log(name)
			}
		}
	})
	.listen(3000)
```

For more information about TypeBox's validator, see [TypeCheck](https://github.com/sinclairzx81/typebox#typecheck).

## Reference Model

Sometimes you might find yourself declaring duplicate models or re-using the same model multiple times.

With a reference model, we can name our model and reuse it by referencing the name.

Let's start with a simple scenario.

Suppose we have a controller that handles sign-in with the same model.

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .post('/sign-in', ({ body }) => body, {
        body: t.Object({
            username: t.String(),
            password: t.String()
        }),
        response: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
```

We can refactor the code by extracting the model as a variable and referencing it.

```typescript
import { Elysia, t } from 'elysia'

// Maybe in a different file eg. models.ts
const SignDTO = t.Object({
    username: t.String(),
    password: t.String()
})

const app = new Elysia()
    .post('/sign-in', ({ body }) => body, {
        body: SignDTO,
        response: SignDTO
    })
```

This method of separating concerns is an effective approach, but we might find ourselves reusing multiple models with different controllers as the app gets more complex.

We can resolve that by creating a "reference model", allowing us to name the model and use auto-completion to reference it directly in `schema` by registering the models with `model`.

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .model({
        sign: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
    .post('/sign-in', ({ body }) => body, {
        // with auto-completion for existing model name
        body: 'sign',
        response: 'sign'
    })
```

When we want to access the model's group, we can separate a `model` into a plugin, which when registered will provide a set of models instead of multiple imports.

```typescript
// auth.model.ts
import { Elysia, t } from 'elysia'

export const authModel = new Elysia()
    .model({
        sign: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
```

Then in an instance file:

```typescript twoslash
// @filename: auth.model.ts
import { Elysia, t } from 'elysia'

export const authModel = new Elysia()
    .model({
        sign: t.Object({
            username: t.String(),
            password: t.String()
        })
    })

// @filename: index.ts
// ---cut---
// index.ts
import { Elysia } from 'elysia'
import { authModel } from './auth.model'

const app = new Elysia()
    .use(authModel)
    .post('/sign-in', ({ body }) => body, {
        // with auto-completion for existing model name
        body: 'sign',
        response: 'sign'
    })
```

This approach not only allows us to separate concerns but also enables us to reuse the model in multiple places while integrating the model into OpenAPI documentation.

### Multiple Models

`model` accepts an object with the key as a model name and the value as the model definition. Multiple models are supported by default.

```typescript
// auth.model.ts
import { Elysia, t } from 'elysia'

export const authModel = new Elysia()
    .model({
        number: t.Number(),
        sign: t.Object({
            username: t.String(),
            password: t.String()
        })
    })
```

### Naming Convention

Duplicate model names will cause Elysia to throw an error. To prevent declaring duplicate model names, we can use the following naming convention.

Let's say that we have all models stored at `models/<name>.ts` and declare the prefix of the model as a namespace.

```typescript
import { Elysia, t } from 'elysia'

// admin.model.ts
export const adminModels = new Elysia()
    .model({
        'admin.auth': t.Object({
            username: t.String(),
            password: t.String()
        })
    })

// user.model.ts
export const userModels = new Elysia()
    .model({
        'user.auth': t.Object({
            username: t.String(),
            password: t.String()
        })
    })
```

This can prevent naming duplication to some extent, but ultimately, it's best to let your team decide on the naming convention.

Elysia provides an opinionated option to help prevent decision fatigue.

### TypeScript

We can get type definitions of every Elysia/TypeBox's type by accessing the `static` property as follows:

```ts twoslash
import { t } from 'elysia'

const MyType = t.Object({
	hello: t.Literal('Elysia')
})

type MyType = typeof MyType.static
//    ^?
```

This allows Elysia to infer and provide type automatically, reducing the need to declare duplicate schema

A single Elysia/TypeBox schema can be used for:

* Runtime validation
* Data coercion
* TypeScript type
* OpenAPI schema

This allows us to make a schema as a **single source of truth**.

---

---
url: 'https://elysiajs.com/tutorial/patterns/validation-error.md'
---

# Validation Error

If you use `Elysia.t` for validation, you can provide a custom error message based on the field that fails the validation.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post(
		'/',
		({ body }) => body,
		{
			body: t.Object({
				age: t.Number({
					error: 'Age must be a number' // [!code ++]
				})
			}, {
				error: 'Body must be an object' // [!code ++]
			})
		}
	)
	.listen(3000)
```

Elysia will override the default error message with the custom one you provide, see Custom Validation Message.

## Validation Detail

By default Elysia also provides a Validation Detail to explain what's wrong with the validation as follows:

```json
{
	"type": "validation",
	"on": "params",
	"value": { "id": "string" },
	"property": "/id",
	"message": "id must be a number", // [!code ++]
	"summary": "Property 'id' should be one of: 'numeric', 'number'",
	"found": { "id": "string" },
	"expected": { "id": 0 },
	"errors": [
		{
			"type": 62,
			"schema": {
				"anyOf": [
					{ "format": "numeric", "default": 0, "type": "string" },
					{ "type": "number" }
				]
			},
			"path": "/id",
			"value": "string",
			"message": "Expected union value",
			"errors": [{ "iterator": {} }, { "iterator": {} }],
			"summary": "Property 'id' should be one of: 'numeric', 'number'"
		}
	]
}
```

However, when you provide a custom error message, it will completely override Validation Detail

To bring back the validation detail, you can wrap your custom error message in a Validation Detail function.

```typescript
import { Elysia, t, validationDetail } from 'elysia' // [!code ++]

new Elysia()
	.post(
		'/',
		({ body }) => body,
		{
			body: t.Object({
				age: t.Number({
					error: validationDetail('Age must be a number') // [!code ++]
				})
			}, {
				error: validationDetail('Body must be an object') // [!code ++]
			})
		}
	)
	.listen(3000)
```

## Assignment

Let's try to extend Elysia's context.

\<template #answer>

We can provide a custom error message by providing `error` property to the schema.

```typescript
import { Elysia, t } from 'elysia'

new Elysia()
	.post(
		'/',
		({ body }) => body,
		{
			body: t.Object({
				age: t.Number({
                    error: 'thing' // [!code ++]
                })
			})
		}
	)
	.listen(3000)
```

---

---
url: 'https://elysiajs.com/patterns/websocket.md'
---

# WebSocket

WebSocket is a real-time protocol for communication between your client and server.

Unlike HTTP where our client repeatedly asks the website for information and waits for a reply each time, WebSocket sets up a direct line where our client and server can send messages back and forth directly, making the conversation quicker and smoother without having to start over with each message.

SocketIO is a popular library for WebSocket, but it is not the only one. Elysia uses [uWebSocket](https://github.com/uNetworking/uWebSockets) which Bun uses under the hood with the same API.

To use WebSocket, simply call `Elysia.ws()`:

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .ws('/ws', {
        message(ws, message) {
            ws.send(message)
        }
    })
    .listen(3000)
```

## WebSocket message validation:

Same as normal routes, WebSockets also accept a **schema** object to strictly type and validate requests.

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia()
    .ws('/ws', {
        // validate incoming message
        body: t.Object({
            message: t.String()
        }),
        query: t.Object({
            id: t.String()
        }),
        message(ws, { message }) {
            // Get schema from `ws.data`
            const { id } = ws.data.query
            ws.send({
                id,
                message,
                time: Date.now()
            })
        }
    })
    .listen(3000)
```

WebSocket schema can validate the following:

* **message** - An incoming message.
* **query** - Query string or URL parameters.
* **params** - Path parameters.
* **header** - Request's headers.
* **cookie** - Request's cookie
* **response** - Value returned from handler

By default Elysia will parse incoming stringified JSON message as Object for validation.

## Configuration

You can set Elysia constructor to set the Web Socket value.

```ts
import { Elysia } from 'elysia'

new Elysia({
    websocket: {
        idleTimeout: 30
    }
})
```

Elysia's WebSocket implementation extends Bun's WebSocket configuration, please refer to [Bun's WebSocket documentation](https://bun.sh/docs/api/websockets) for more information.

The following is a brief configuration from [Bun WebSocket](https://bun.sh/docs/api/websockets#create-a-websocket-server)

### perMessageDeflate

@default `false`

Enable compression for clients that support it.

By default, compression is disabled.

### maxPayloadLength

The maximum size of a message.

### idleTimeout

@default `120`

After a connection has not received a message for this many seconds, it will be closed.

### backpressureLimit

@default `16777216` (16MB)

The maximum number of bytes that can be buffered for a single connection.

### closeOnBackpressureLimit

@default `false`

Close the connection if the backpressure limit is reached.

## Methods

Below are the new methods that are available to the WebSocket route

## ws

Create a websocket handler

Example:

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
    .ws('/ws', {
        message(ws, message) {
            ws.send(message)
        }
    })
    .listen(3000)
```

Type:

```typescript
.ws(endpoint: path, options: Partial<WebSocketHandler<Context>>): this
```

* **endpoint** - A path to be exposed as websocket handler
* **options** - Customize WebSocket handler behavior

## WebSocketHandler

WebSocketHandler extends config from [config](#configuration).

Below is a config which is accepted by `ws`.

## open

Callback function for new websocket connection.

Type:

```typescript
open(ws: ServerWebSocket<{
    // uid for each connection
    id: string
    data: Context
}>): this
```

## message

Callback function for incoming websocket message.

Type:

```typescript
message(
    ws: ServerWebSocket<{
        // uid for each connection
        id: string
        data: Context
    }>,
    message: Message
): this
```

`Message` type based on `schema.message`. Default is `string`.

## close

Callback function for closing websocket connection.

Type:

```typescript
close(ws: ServerWebSocket<{
    // uid for each connection
    id: string
    data: Context
}>): this
```

## drain

Callback function for the server is ready to accept more data.

Type:

```typescript
drain(
    ws: ServerWebSocket<{
        // uid for each connection
        id: string
        data: Context
    }>,
    code: number,
    reason: string
): this
```

## parse

`Parse` middleware to parse the request before upgrading the HTTP connection to WebSocket.

## beforeHandle

`Before Handle` middleware which execute before upgrading the HTTP connection to WebSocket.

Ideal place for validation.

## transform

`Transform` middleware which execute before validation.

## transformMessage

Like `transform`, but execute before validation of WebSocket message

## header

Additional headers to add before upgrading connection to WebSocket.

---

---
url: 'https://elysiajs.com/tutorial/whats-next.md'
---

# Congratulations!

You have completed the tutorial.

Now you're ready to build your own application with Elysia!

## First up

We highly recommend that you check out these 2 pages first before getting started with Elysia:

### llms.txt

Alternatively, you can download llms.txt or llms-full.txt and feed it to your favorite LLMs like ChatGPT, Claude or Gemini to get a more interactive experience.

### If you are stuck

Feel free to ask our community on GitHub Discussions, Discord, and Twitter.

## From another Framework?

If you have used other popular frameworks like Express, Fastify, or Hono, you will find Elysia right at home with just a few differences.

## Essential Chapter

Here are the foundations of Elysia, we highly recommend that you go through these pages before jumping to other topics:

## More Patterns

If you feel like exploring more Elysia features, check out:

## Integration with Meta Framework

We can also use Elysia with Meta Framework like Nextjs, Nuxt, Astro, etc.

## Integration with your favorite tool

We have some integration with popular tools:

***

We hope you will love Elysia as much as we do!

---

---
url: 'https://elysiajs.com/tutorial/getting-started/your-first-route.md'
---

# Your First Route

When we enter a website, it takes

1. **path** like `/`, `/about`, or `/contact`
2. **method** like `GET`, `POST`, or `DELETE`

To determine which resource to show, simply called **"route"**.

In Elysia, we can define a route by:

1. Call method named after HTTP method
2. Path being the first argument
3. Handler being the second argument

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/', 'Hello World!')
	.listen(3000)
```

## Routing

Path in Elysia can be grouped into 3 types:

1. static paths - static string to locate the resource
2. dynamic paths - segment can be any value
3. wildcards - path until a specific point can be anything

See Route.

## Static Path

Static path is a hardcoded string to locate the resource on the server.

```ts
import { Elysia } from 'elysia'

new Elysia()
	.get('/hello', 'hello')
	.get('/hi', 'hi')
	.listen(3000)
```

See Static Path.

## Dynamic path

Dynamic paths match some part and capture the value to extract extra information.

To define a dynamic path, we can use a colon `:` followed by a name.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id', ({ params: { id } }) => id)
    .listen(3000)
```

Here, a dynamic path is created with `/id/:id`, which tells Elysia to capture the value `:id` segment with value like **/id/1**, **/id/123**, **/id/anything**.

See Dynamic Path.

### Optional path parameters

We can make a path parameter optional by adding a question mark `?` after the parameter name.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/:id?', ({ params: { id } }) => `id ${id}`)
    .listen(3000)
```

See Optional Path Parameters.

## Wildcards

Dynamic paths allow capturing a single segment while wildcards allow capturing the rest of the path.

To define a wildcard, we can use an asterisk `*`.

```typescript
import { Elysia } from 'elysia'

new Elysia()
    .get('/id/*', ({ params }) => params['*'])
    .listen(3000)
```

See Wildcards.

## Assignment

Let's recap, and create 3 paths with different types:

\<template #answer>

1. Static path `/elysia` that responds with `"Hello Elysia!"`
2. Dynamic path `/friends/:name?` that responds with `"Hello {name}!"`
3. Wildcard path `/flame-chasers/*` that responds with the rest of the path.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/elysia', 'Hello Elysia!')
	.get('/friends/:name?', ({ params: { name } }) => `Hello ${name}!`)
	.get('/flame-chasers/*', ({ params }) => params['*'])
	.listen(3000)
```
