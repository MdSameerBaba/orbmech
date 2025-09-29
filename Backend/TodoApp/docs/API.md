# TodoApp API Documentation\n\n## Authentication Endpoints\n\n### POST /api/auth/register\nRegister new user\n\n**Request Body:**\n```json\n{
  "email": "string",
  "password": "string",
  "firstName": "string",
  "lastName": "string"
}\n```\n\n**Response:**\n```json\n{
  "user": "User",
  "token": "string"
}\n```\n\n### POST /api/auth/login\nLogin user\n\n**Request Body:**\n```json\n{
  "email": "string",
  "password": "string"
}\n```\n\n**Response:**\n```json\n{
  "user": "User",
  "token": "string"
}\n```\n\n### GET /api/auth/profile\nGet user profile\n\n**Response:**\n```json\n{
  "user": "User"
}\n```\n\n## API Endpoints\n\n### GET /api/todos\nGet all todos\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "todos": "Array<Todo>"
}\n```\n\n### POST /api/todos\nCreate new todo\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "title": "string",
  "description": "text",
  "completed": "boolean",
  "priority": "string",
  "dueDate": "datetime",
  "userId": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "todo": "Todo"
}\n```\n\n### PUT /api/todos/:id\nUpdate todo\n\n🔒 **Authentication Required**\n\n**Request Body:**\n```json\n{
  "title": "string",
  "description": "text",
  "completed": "boolean",
  "priority": "string",
  "dueDate": "datetime",
  "userId": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}\n```\n\n**Response:**\n```json\n{
  "todo": "Todo"
}\n```\n\n### DELETE /api/todos/:id\nDelete todo\n\n🔒 **Authentication Required**\n\n**Response:**\n```json\n{
  "message": "string"
}\n```\n\n