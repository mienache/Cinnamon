thread main_thread;
thread checker_thread;
uint64 inst_count = 0;

init {
   register_thread(main_thread, "main");
}

select inst I where ((I.opcode) == Load) {
   before I {
       inst_count = inst_count + 1;
   }
}

select func F where (F.isMain) {
   entry F {
      register_thread(checker_thread, "worker");
      run_thread(checker_thread);
   }
}

exit{
   print_u64(inst_count);
}
