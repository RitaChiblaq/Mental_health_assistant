module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  testMatch: ['**/tests/**/*.spec.js'],
  transform: {
    '^.+\\.vue$': 'vue-jest'
  }
};