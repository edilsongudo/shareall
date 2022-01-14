var home = {
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
        </div>`,
            data() {
                return {
                current_dir: "",
                media: [],
                parent_dir: "",
                parent_dir_url: ""
            }
            },

            delimiters: ['[[', ']]'],

            methods: {
                requestFolders: function(url) {
                console.log(`Ajax Call to url ${url}`)

                var state = this //ok THIS IS TO MUCH! REFACTOR THIS

                $.ajax({
                    dataType: 'json',
                    url: url,
                    data: {'ajax': true},
                    success: function (res) {
                        state.current_dir = res.current_dir
                        state.media = res.media
                        state.parent_dir = res.parent_dir
                        state.parent_dir_url = res.parent_dir_url
                    }
                })
            },
                updateUI: function (e) {
                    let is_folder = e.target.querySelector('i.fa-folder')
                    let url = e.target.querySelector('a').href

                    if (is_folder) {
                        e.preventDefault()
                        this.requestFolders(url)
                    } else {
                        window.open(url)
                    }

                },

            },

            created() {
                this.requestFolders(window.origin)
            }
}
