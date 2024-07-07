import { shallowMount, createLocalVue } from '@vue/test-utils';
import App from '@/App.vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';
import Chat from '@/views/Chat.vue';

const localVue = createLocalVue();
localVue.use(VueRouter);

const routes = [
  { path: '/', component: Home },
  { path: '/chat', component: Chat }
];

const router = new VueRouter({ routes });

describe('App.vue', () => {
  it('renders the router view', () => {
    const wrapper = shallowMount(App, {
      localVue,
      router
    });
    expect(wrapper.find('router-view').exists()).toBe(true);
  });
});