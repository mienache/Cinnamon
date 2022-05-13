thread main_thread;
thread checker_thread;
comet_queue COMET_QUEUE;

init {
   register_thread(main_thread, "main");
   COMET_QUEUE = initialise_comet_queue();
}

select func F where (F.isMain) {
   entry F {
      enable_thread_specific(main_thread);

      register_thread(checker_thread, "worker");
      run_thread(checker_thread);
   }
}

select func F where (F.isMain) {
   exit F {
      enable_thread_specific(main_thread);

      wait_for_checker_thread();
   }
}

select func F where (F.isMain) {
   exit F {
      enable_thread_specific(checker_thread);

      mark_checker_thread_finished();
   }
}

select inst I where (I.needsCometInstrumentation) {
   at I {
      enable_thread_specific(main_thread);

      enqueue(COMET_QUEUE);
   }
}

select inst I where (I.needsCometInstrumentation) {
   at I {
      enable_thread_specific(checker_thread);

      dequeue_expect(COMET_QUEUE);

   }
}
