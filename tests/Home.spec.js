import { shallowMount, createLocalVue } from '@vue/test-utils';
import Home from '@/views/Home.vue';
import VueRouter from 'vue-router';

const localVue = createLocalVue();
localVue.use(VueRouter);

describe('Home.vue', () => {
  it('renders home view', () => {
    const wrapper = shallowMount(Home);
    expect(wrapper.find('h1').text()).toBe('Your Mental Assistant');
  });

  it('navigates to /chat when Start button is clicked', async () => {
    const router = new VueRouter();
    const wrapper = shallowMount(Home, {
      localVue,
      router
    });
    const startButton = wrapper.find('.start-button');
    await startButton.trigger('click');
    expect(wrapper.vm.$route.path).toBe('/chat');
  });
});