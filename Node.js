const fs = require('fs');

const privateKeyPath = 'C:/Users/Ms-Echo/Documents/GitHub/SET-Protocol/userprivate.pem';

try {
  // Read the contents of the userprivate.pem file
  const privateKey = fs.readFileSync(privateKeyPath, 'utf8');

  // Check if the key starts with '-----BEGIN RSA PRIVATE KEY-----' and ends with '-----END RSA PRIVATE KEY-----'
  const isPrivateKeyValid =
    privateKey.startsWith('-----BEGIN RSA PRIVATE KEY-----') &&
    privateKey.endsWith('-----END RSA PRIVATE KEY-----');

  // Print the result
  console.log('Is the private key valid?', isPrivateKeyValid);
} catch (error) {
  console.error('Error reading or validating the private key:', error.message);
}