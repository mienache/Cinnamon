thread main_thread;
thread checker_thread;
uint64 inst_count = 0;
comet_queue queue;

init {
   register_thread(main_thread, "main");
   queue = initialise_queue();
}

select inst I where ((I.opcode) == Load) {
   before I {
      inst_count = inst_count + 1;
   }
}

select func F where (F.isMain) {
   entry F {
      enable_thread_specific(main_thread);

      register_thread(checker_thread, "worker");
      run_thread(checker_thread);
   }
}

select inst I where ((I.opcode) == Load) {
   at I {
      enable_thread_specific(main_thread);

      if(I.num_dst_opnds) {
         queue.enqueue(I.dst);
      }
   }
}

select inst I where ((I.opcode) == Load) {
   at I {
      enable_thread_specific(checker_thread);

      if(I.num_dst_opnds) {
         queue.dequeue_expect(I.dst);
      }
   }
}

exit{
   print_u64(inst_count);
}
