var Home = {
    template:
    `
        <div class="container">
            <div style="margin-bottom: 30px;">[[current_dir]]</div>

            <div class="media_element" @click="updateUI">
                <div style="pointer-events: none;">
                    <a :href="parent_dir_url" >
                        <div><i class="fas fa-folder"></i></div>
                        <div class="text">Parent Dir</div>
                    </a>
                </div>
            </div>

            <div class="media_container">
                    <div class="media_element" v-for="m in media" @click="updateUI">
                        <div style="pointer-events: none;">
                            <a class="link" :href="m.url">
                                <div>
                                    <div v-if="m.is_dir === true">
                                        <i class="fas fa-folder"></i>
                                    </div>
                                    <div v-else>
                                        <i :class="m.extension_icon"></i>
                                    </div>
                                    <div>
                                        <div class="text">[[ m.filename ]]</div>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>
             </div>
        </div>`
}
