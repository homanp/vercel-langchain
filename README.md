
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhomanp%2Fvercel-langchain)

# LangChain running on Vercel

A minimal example on how to run LangChain on Vercel using Flask.

## Installation

#### 1. Virtualenv
Create and activate `virtualenv`.

```bash
virtualenv MY_ENV
source MY_ENV/bin/activate
```

#### 2. Install requirements
```bash
pip install -r requirements.txt
```

#### 3. Start development server
```bash
vercel dev
```

#### 4. Example API route
```bash
GET http://localhost:3000
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY`

## One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhomanp%2Fvercel-langchain)



## Further reading

Learn more about how to use LangChain by visiting the offical documentation or repo:

https://langchain.readthedocs.io/en/latest/

https://github.com/hwchase17/langchain
