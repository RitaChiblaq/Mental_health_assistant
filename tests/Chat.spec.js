import { shallowMount } from '@vue/test-utils';
import Chat from '@/views/Chat.vue';

describe('Chat.vue', () => {
  it('renders chat iframe', () => {
    const wrapper = shallowMount(Chat);
    expect(wrapper.find('iframe').exists()).toBe(true);
  });
});