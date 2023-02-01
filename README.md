
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
pip install requirements.txt
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


## Further reading

Learn more about how to use LangChain by visiting the offical documentation or repo:

https://langchain.readthedocs.io/en/latest/

https://github.com/hwchase17/langchain

